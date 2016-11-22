#include "Math/Minimizer.h"
#include "Math/Factory.h"
#include "Math/Functor.h"
#include "TRandom2.h"
#include "TError.h"
#include "TFile.h"
#include "TH1.h"
#include "THStack.h"
#include "TCanvas.h"
#include "Fit/ParameterSettings.h"
#include <iostream>

void charge_flip_truth(){


  /*TFile* OS2Prompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSBothPromp_Powheg.root");
  TFile* OS2NonPrompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSBothNonPromp_Powheg.root");
  TFile* OSCHF1   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSCHF1_Powheg.root");
  TFile* OSCHF2   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSCHF2_Powheg.root");
  TFile* OSBrem   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSBrem_Powheg.root");
  TFile* OSFSR   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSFSR_Powheg.root");
  TFile* OSFake   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeOSFake_Powheg.root");

  TFile* SS2Prompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSBothPromp_Powheg.root");
  TFile* SS2NonPrompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSBothNonPromp_Powheg.root");
  TFile* SSCHF1   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSCHF1_Powheg.root");
  TFile* SSCHF2   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSCHF2_Powheg.root");
  TFile* SSBrem   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSBrem_Powheg.root");
  TFile* SSFSR   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSFSR_Powheg.root");
  TFile* SSFake   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMass_ZeeSSFake_Powheg.root");*/

  TFile* OS2Prompt   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSBothPromp_CHFTruth1.root");
  TFile* OS2NonPrompt   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSBothNonPromp_CHFTruth1.root");
  TFile* OSCHF1   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSCHF1_CHFTruth1.root");
  TFile* OSCHF2   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSCHF2_CHFTruth1.root");
  TFile* OSBrem   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSBrem_CHFTruth1.root");
  TFile* OSFSR   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSFSR_CHFTruth1.root");
  TFile* OSFake   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeOSFake_CHFTruth1.root");

  TFile* SS2Prompt   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSBothPromp_CHFTruth1.root");
  TFile* SS2NonPrompt   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSBothNonPromp_CHFTruth1.root");
  TFile* SSCHF1   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSCHF1_CHFTruth1.root");
  TFile* SSCHF2   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSCHF2_CHFTruth1.root");
  TFile* SSBrem   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSBrem_CHFTruth1.root");
  TFile* SSFSR   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSFSR_CHFTruth1.root");
  TFile* SSFake   = new TFile("/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_invMass_ZeeSSFake_CHFTruth1.root");

  TH1F* hOS2Prompt = (TH1F*) OS2Prompt->Get("h_ZeeOSBothPromp_nominal_Zee");
  TH1F* hOS2NonPrompt = (TH1F*) OS2NonPrompt->Get("h_ZeeOSBothNonPromp_nominal_Zee");
  TH1F* hOSCHF1 = (TH1F*) OSCHF1->Get("h_ZeeOSCHF1_nominal_Zee");
  TH1F* hOSCHF2 = (TH1F*) OSCHF2->Get("h_ZeeOSCHF2_nominal_Zee");
  TH1F* hOSBrem = (TH1F*) OSBrem->Get("h_ZeeOSBrem_nominal_Zee");
  TH1F* hOSFSR = (TH1F*) OSFSR->Get("h_ZeeOSFSR_nominal_Zee");
  TH1F* hOSFake = (TH1F*) OSFake->Get("h_ZeeOSFake_nominal_Zee");

  TH1F* hSS2Prompt = (TH1F*) SS2Prompt->Get("h_ZeeSSBothPromp_nominal_Zee");
  TH1F* hSS2NonPrompt = (TH1F*) SS2NonPrompt->Get("h_ZeeSSBothNonPromp_nominal_Zee");
  TH1F* hSSCHF1 = (TH1F*) SSCHF1->Get("h_ZeeSSCHF1_nominal_Zee");
  TH1F* hSSCHF2 = (TH1F*) SSCHF2->Get("h_ZeeSSCHF2_nominal_Zee");
  TH1F* hSSBrem = (TH1F*) SSBrem->Get("h_ZeeSSBrem_nominal_Zee");
  TH1F* hSSFSR = (TH1F*) SSFSR->Get("h_ZeeSSFSR_nominal_Zee");
  TH1F* hSSFake = (TH1F*) SSFake->Get("h_ZeeSSFake_nominal_Zee");

  hOS2Prompt->SetFillColor(kWhite);
  hOS2NonPrompt->SetFillColor(kGray);
  hOSCHF1->SetFillColor(kBlue-2);
  hOSCHF2->SetFillColor(kBlue-4);
  hOSBrem->SetFillColor(kOrange);
  hOSFSR->SetFillColor(kRed-2);
  hOSFake->SetFillColor(kRed-3);

  hSS2Prompt->SetFillColor(kWhite);
  hSS2NonPrompt->SetFillColor(kGray);
  hSSCHF1->SetFillColor(kBlue-2);
  hSSCHF2->SetFillColor(kBlue-4);
  hSSBrem->SetFillColor(kOrange);
  hSSFSR->SetFillColor(kRed-2);
  hSSFake->SetFillColor(kRed-3);

  THStack* hsOS = new THStack("hsOS","hsOS");
  hsOS->Add(hOS2NonPrompt);
  hsOS->Add(hOSFake);
  hsOS->Add(hOSFSR);
  hsOS->Add(hOSBrem);
  hsOS->Add(hOSCHF2);
  hsOS->Add(hOSCHF1);
  hsOS->Add(hOS2Prompt);

  THStack* hsSS = new THStack("hsSS","hsSS");
  hsSS->Add(hSS2NonPrompt);
  hsSS->Add(hSSFake);
  hsSS->Add(hSSFSR);
  hsSS->Add(hSSBrem);
  hsSS->Add(hSSCHF2);
  hsSS->Add(hSSCHF1);
  hsSS->Add(hSS2Prompt);

  TH1F* hSSCHF1Clone = (TH1F*) hSSCHF1->Clone();
  TH1F* hSSCHF2Clone = (TH1F*) hSSCHF2->Clone();
  /*for (int i = 5; i <= hSSCHF1Clone->GetNbinsX(); i++){
    hSSCHF1Clone->SetBinContent(i, hSSCHF1Clone->GetBinContent(i)/hSSCHF2Clone->GetBinContent(i-4) );
    hSSCHF1Clone->SetBinError(i, sqrt(pow(hSSCHF1Clone->GetBinError(i),2)+pow(hSSCHF2Clone->GetBinError(i-4),2))/hSSCHF1->GetBinContent(i) );
  }*/
  hSSCHF1Clone->Divide(hSSCHF2Clone);

  // legend
  TLegend* leg = new TLegend(0.60,0.700,0.95,0.92);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  leg->SetFillStyle(0);
  leg->SetTextSize(0.03);
  leg->AddEntry(hSS2Prompt,"2 prompt","f");
  leg->AddEntry(hSSCHF1,"charge-flip type 1","f");
  leg->AddEntry(hSSCHF2,"charge-flip type 2","f");
  leg->AddEntry(hSSBrem,"brem","f");
  leg->AddEntry(hSSFSR,"FSR","f");
  leg->AddEntry(hSSFake,"other","f");
  leg->AddEntry(hSS2NonPrompt,"2 non-prompt","f");

  TCanvas c1("c1","c1",600,600);
  c1.SetLogy();
  c1.SetLogx();
  hsOS->Draw("hist");
  hsOS->SetMinimum(1e-2);
  hsOS->SetMaximum(1e6);
  hsOS->GetXaxis()->SetTitle("m(e^{#pm}e^{#mp})");
  hsOS->GetYaxis()->SetTitle("Events");
  hsOS->GetXaxis()->SetNoExponent();
  hsOS->GetXaxis()->SetMoreLogLabels();

  //hsOS->GetXaxis()->SetRangeUser(50,130);

  leg->Draw();
  ATLASLabel(0.18,0.88,"internal",1);
  myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}");
  myText(0.18,0.77,1,"Powheg Z#rightarrow ee");
  myText(0.18,0.72,1,"abs(#eta) < 2.1");

  TCanvas c2("c2","c2",600,600);
  c2.SetLogy();
  c2.SetLogx();
  hsSS->Draw("hist");
  hsSS->SetMinimum(1e-2);
  hsSS->SetMaximum(1e6);
  hsSS->GetXaxis()->SetTitle("m(e^{#pm}e^{#pm})");
  hsSS->GetYaxis()->SetTitle("Events");
  hsSS->GetXaxis()->SetNoExponent();
  hsSS->GetXaxis()->SetMoreLogLabels();

  //hsSS->GetXaxis()->SetRangeUser(50,130);

  leg->Draw();
  ATLASLabel(0.18,0.88,"internal",1);
  myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}");
  myText(0.18,0.77,1,"Powheg Z#rightarrow ee");
  myText(0.18,0.72,1,"abs(#eta) < 2.1");

  TCanvas c3("c3","c3",600,600);
  //c3.SetLogy();
  c3.SetLogx();
  hSSCHF1Clone->Draw("ep0");
  hSSCHF1Clone->GetYaxis()->SetRangeUser(0,2);
  hSSCHF1Clone->GetYaxis()->SetTitle("CHF type-1 / CHF type-2");
  hSSCHF1Clone->GetXaxis()->SetTitle("m(e^{#pm}e^{#pm})");
  hSSCHF1Clone->GetXaxis()->SetNoExponent();
  hSSCHF1Clone->GetXaxis()->SetMoreLogLabels();
  ATLASLabel(0.18,0.88,"internal",1);
  myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}");
  myText(0.18,0.77,1,"Powheg Z#rightarrow ee");
  myText(0.18,0.72,1,"abs(#eta) < 2.1");

  //hSSCHF1Clone->GetXaxis()->SetRangeUser(50,130);


  c1.Print("cOS-CHF1.eps");
  c2.Print("cSS-CHF1.eps");
  c3.Print("cRatio-CHF1.eps");



}