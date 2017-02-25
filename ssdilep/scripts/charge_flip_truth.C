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


  /*TFile* OS2Prompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSBothPromp_Powheg.root");
  TFile* OS2NonPrompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSBothNonPromp_Powheg.root");
  TFile* OSCHF1   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSCHF1_Powheg.root");
  TFile* OSCHF2   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSCHF2_Powheg.root");
  TFile* OSBrem   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSBrem_Powheg.root");
  TFile* OSFSR   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSFSR_Powheg.root");
  TFile* OSFake   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeOSFake_Powheg.root");

  TFile* SS2Prompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSBothPromp_Powheg.root");
  TFile* SS2NonPrompt   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSBothNonPromp_Powheg.root");
  TFile* SSCHF1   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSCHF1_Powheg.root");
  TFile* SSCHF2   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSCHF2_Powheg.root");
  TFile* SSBrem   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSBrem_Powheg.root");
  TFile* SSFSR   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSFSR_Powheg.root");
  TFile* SSFake   = new TFile("/ceph/grid/home/atlas/miham/storage/PlotsCHFTruthPowheg/hists_invMassLong_ZeeSSFake_Powheg.root");*/

  TFile* el_pt_eta_chf2_ZeeSS130M300CHF1_SherpaTrueCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf2_ZeeSS130M300CHF1_SherpaTrueCHF.root");
  TFile* el_pt_eta_chf4_ZeeSS130M300CHF2_SherpaTrueCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf4_ZeeSS130M300CHF2_SherpaTrueCHF.root");
  TFile* el_pt_eta_chf2_ZeeSS300M1200CHF1_SherpaTrueCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf2_ZeeSS300M1200CHF1_SherpaTrueCHF.root");
  TFile* el_pt_eta_chf4_ZeeSS300M1200CHF2_SherpaTrueCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf4_ZeeSS300M1200CHF2_SherpaTrueCHF.root");
  TFile* el_pt_eta_chf2_ZeeSS1200MCHF1_SherpaTrueCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf2_ZeeSS1200MCHF1_SherpaTrueCHF.root");
  TFile* el_pt_eta_chf4_ZeeSS1200MCHF2_SherpaTrueCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_el_pt_eta_chf4_ZeeSS1200MCHF2_SherpaTrueCHF.root");

  TH2F* hists_el_pt_eta_chf2_ZeeSS130M300CHF1_SherpaTrueCHF   = (TH2F*) el_pt_eta_chf2_ZeeSS130M300CHF1_SherpaTrueCHF->Get("h_ZeeSS130M300CHF1_nominal_Zee");
  TH2F* hists_el_pt_eta_chf4_ZeeSS130M300CHF2_SherpaTrueCHF   = (TH2F*) el_pt_eta_chf4_ZeeSS130M300CHF2_SherpaTrueCHF->Get("h_ZeeSS130M300CHF2_nominal_Zee");
  TH2F* hists_el_pt_eta_chf2_ZeeSS300M1200CHF1_SherpaTrueCHF   = (TH2F*) el_pt_eta_chf2_ZeeSS300M1200CHF1_SherpaTrueCHF->Get("h_ZeeSS300M1200CHF1_nominal_Zee");
  TH2F* hists_el_pt_eta_chf4_ZeeSS300M1200CHF2_SherpaTrueCHF   = (TH2F*) el_pt_eta_chf4_ZeeSS300M1200CHF2_SherpaTrueCHF->Get("h_ZeeSS300M1200CHF2_nominal_Zee");
  TH2F* hists_el_pt_eta_chf2_ZeeSS1200MCHF1_SherpaTrueCHF   = (TH2F*) el_pt_eta_chf2_ZeeSS1200MCHF1_SherpaTrueCHF->Get("h_ZeeSS1200MCHF1_nominal_Zee");
  TH2F* hists_el_pt_eta_chf4_ZeeSS1200MCHF2_SherpaTrueCHF   = (TH2F*) el_pt_eta_chf4_ZeeSS1200MCHF2_SherpaTrueCHF->Get("h_ZeeSS1200MCHF2_nominal_Zee");

  TH2F* hCHF130M300 = (TH2F*) hists_el_pt_eta_chf2_ZeeSS130M300CHF1_SherpaTrueCHF->Clone();
  hCHF130M300->Add(hists_el_pt_eta_chf4_ZeeSS130M300CHF2_SherpaTrueCHF);
  TH2F* hCHF300M1200 = (TH2F*) hists_el_pt_eta_chf2_ZeeSS300M1200CHF1_SherpaTrueCHF->Clone();
  hCHF300M1200->Add(hists_el_pt_eta_chf4_ZeeSS300M1200CHF2_SherpaTrueCHF);
  TH2F* hCHFM1200 = (TH2F*) hists_el_pt_eta_chf2_ZeeSS1200MCHF1_SherpaTrueCHF->Clone();
  hCHFM1200->Add(hists_el_pt_eta_chf4_ZeeSS1200MCHF2_SherpaTrueCHF);

  TFile* OSAll   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOS_CHFTruth1.root");
  TFile* OS2Prompt   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSBothPromp_CHFTruth1.root");
  TFile* OS2NonPrompt   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSBothNonPromp_CHFTruth1.root");
  TFile* OSCHF1   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSCHF1_CHFTruth1.root");
  TFile* OSCHF2   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSCHF2_CHFTruth1.root");
  TFile* OSBrem   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSBrem_CHFTruth1.root");
  TFile* OSFSR   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSFSR_CHFTruth1.root");
  TFile* OSFake   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeOSFake_CHFTruth1.root");

  TFile* SSAll   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSS_CHFTruth1.root");
  TFile* SS2Prompt   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSBothPromp_CHFTruth1.root");
  TFile* SS2NonPrompt   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSBothNonPromp_CHFTruth1.root");
  TFile* SSCHF1   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSCHF1_CHFTruth1.root");
  TFile* SSCHF1SF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSCHF1SF_CHFTruth1.root");
  TFile* SSCHF2   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSCHF2_CHFTruth1.root");
  TFile* SSCHF2SF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSCHF2SF_CHFTruth1.root");
  TFile* SSBrem   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSBrem_CHFTruth1.root");
  TFile* SSFSR   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSFSR_CHFTruth1.root");
  TFile* SSFake   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeSSFake_CHFTruth1.root");

  TFile* BothCHF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeBothCHF_CHFTruth1.root");
  TFile* BothCHFSF   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak36/hists_invMassLong_ZeeBothCHFSF_CHFTruth1.root");

  TH1F* hOSAll = (TH1F*) OSAll->Get("h_ZeeOS_nominal_Zee");
  TH1F* hOS2Prompt = (TH1F*) OS2Prompt->Get("h_ZeeOSBothPromp_nominal_Zee");
  TH1F* hOS2NonPrompt = (TH1F*) OS2NonPrompt->Get("h_ZeeOSBothNonPromp_nominal_Zee");
  TH1F* hOSCHF1 = (TH1F*) OSCHF1->Get("h_ZeeOSCHF1_nominal_Zee");
  TH1F* hOSCHF2 = (TH1F*) OSCHF2->Get("h_ZeeOSCHF2_nominal_Zee");
  TH1F* hOSBrem = (TH1F*) OSBrem->Get("h_ZeeOSBrem_nominal_Zee");
  TH1F* hOSFSR = (TH1F*) OSFSR->Get("h_ZeeOSFSR_nominal_Zee");
  TH1F* hOSFake = (TH1F*) OSFake->Get("h_ZeeOSFake_nominal_Zee");

  TH1F* hSSAll = (TH1F*) SSAll->Get("h_ZeeSS_nominal_Zee");
  TH1F* hSS2Prompt = (TH1F*) SS2Prompt->Get("h_ZeeSSBothPromp_nominal_Zee");
  TH1F* hSS2NonPrompt = (TH1F*) SS2NonPrompt->Get("h_ZeeSSBothNonPromp_nominal_Zee");
  TH1F* hSSCHF1 = (TH1F*) SSCHF1->Get("h_ZeeSSCHF1_nominal_Zee");
  TH1F* hSSCHF1SF = (TH1F*) SSCHF1SF->Get("h_ZeeSSCHF1SF_nominal_Zee");
  TH1F* hSSCHF2 = (TH1F*) SSCHF2->Get("h_ZeeSSCHF2_nominal_Zee");
  TH1F* hSSCHF2SF = (TH1F*) SSCHF2SF->Get("h_ZeeSSCHF2SF_nominal_Zee");
  TH1F* hSSBrem = (TH1F*) SSBrem->Get("h_ZeeSSBrem_nominal_Zee");
  TH1F* hSSFSR = (TH1F*) SSFSR->Get("h_ZeeSSFSR_nominal_Zee");
  TH1F* hSSFake = (TH1F*) SSFake->Get("h_ZeeSSFake_nominal_Zee");

  TH1F* hBothCHF = (TH1F*) BothCHF->Get("h_ZeeBothCHF_nominal_Zee");
  TH1F* hBothCHFSF = (TH1F*) BothCHFSF->Get("h_ZeeBothCHFSF_nominal_Zee");

  TH1F* hAll = (TH1F*) hOSAll->Clone();
  hAll->Add(hSSAll);
  TH1F* hCHF = (TH1F*) hSSCHF1->Clone();
  hCHF->Add(hSSCHF2);
  TH1F* hCHFSF = (TH1F*) hSSCHF1SF->Clone();
  hCHFSF->Add(hSSCHF2SF);
  TH1F* hCHFr = (TH1F*) hCHF->Clone();
  hCHFr->Divide(hAll);
  TH1F* hCHFSFr = (TH1F*) hCHFSF->Clone();
  hCHFSFr->Divide(hAll);

  TH1F* hAllRebin = (TH1F*) hAll->Clone();
  hAllRebin->Rebin(10);
  TH1F* hBothCHFr = (TH1F*) hBothCHF->Clone();
  hBothCHFr->Rebin(10);
  hBothCHFr->Divide(hAllRebin);
  TH1F* hBothCHFSFr = (TH1F*) hBothCHFSF->Clone();
  hBothCHFSFr->Rebin(10);
  hBothCHFSFr->Divide(hAllRebin);

  hCHFr->SetMarkerSize(0.6);
  hCHFr->SetMarkerColor(kRed);
  hCHFr->SetLineColor(kRed);
  hCHFSFr->SetMarkerSize(0.6);

  hCHFr->GetXaxis()->SetRangeUser(130,7000);
  hCHFr->Scale(100.);
  hCHFSFr->GetXaxis()->SetRangeUser(130,7000);
  hCHFSFr->Scale(100.);

  hBothCHFr->SetMarkerSize(0.6);
  hBothCHFr->SetMarkerColor(kRed+2);
  hBothCHFr->SetLineColor(kRed+2);
  hBothCHFSFr->SetMarkerSize(0.6);
  hBothCHFSFr->SetMarkerColor(kBlue+2);
  hBothCHFSFr->SetLineColor(kBlue+2);

  hBothCHFr->GetXaxis()->SetRangeUser(130,7000);
  hBothCHFr->Scale(100.);
  hBothCHFSFr->GetXaxis()->SetRangeUser(130,7000);
  hBothCHFSFr->Scale(100.);

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
  leg->AddEntry(hSSCHF1,"charge-flip type 2","f");
  leg->AddEntry(hSSCHF2,"charge-flip type 4","f");
  leg->AddEntry(hSSBrem,"brem","f");
  leg->AddEntry(hSSFSR,"FSR","f");
  leg->AddEntry(hSSFake,"other","f");
  leg->AddEntry(hSS2NonPrompt,"2 non-prompt","f");

  TLegend* leg2 = new TLegend(0.18,0.45,0.5,0.70);
  leg2->SetBorderSize(0);
  leg2->SetFillColor(0);
  leg2->SetFillStyle(0);
  leg2->SetTextSize(0.045);
  leg2->AddEntry(hCHFr,  "#font[42]{one flip}","pe");
  leg2->AddEntry(hCHFSFr,"#font[42]{one flip with SF}","pe");
  leg2->AddEntry(hBothCHFr,"#font[42]{both flip}","pe0");
  leg2->AddEntry(hBothCHFSFr,"#font[42]{both flip with SF}","pe");

  TCanvas c1("c1","c1",600,600);
  c1.SetLogy();
  c1.SetLogx();
  hsOS->Draw("hist");
  hsOS->SetMinimum(1e-7);
  hsOS->SetMaximum(1e7);
  hsOS->GetXaxis()->SetTitle("m(e^{#pm}e^{#mp})");
  hsOS->GetYaxis()->SetTitle("Entries");
  hsOS->GetXaxis()->SetNoExponent();
  hsOS->GetXaxis()->SetMoreLogLabels();

  //hsOS->GetXaxis()->SetRangeUser(50,130);

  leg->Draw();
  ATLASLabel(0.18,0.88,"internal",1);
  myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 36.5 fb^{-1}");
  myText(0.18,0.77,1,"Powheg Z#rightarrow ee");

  TCanvas c2("c2","c2",600,600);
  c2.SetLogy();
  c2.SetLogx();
  hsSS->Draw("hist");
  hsSS->SetMinimum(1e-7);
  hsSS->SetMaximum(1e7);
  hsSS->GetXaxis()->SetTitle("m(e^{#pm}e^{#pm})");
  hsSS->GetYaxis()->SetTitle("Entries");
  hsSS->GetXaxis()->SetNoExponent();
  hsSS->GetXaxis()->SetMoreLogLabels();

  //hsSS->GetXaxis()->SetRangeUser(50,130);

  leg->Draw();
  ATLASLabel(0.18,0.88,"internal",1);
  myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 36.5 fb^{-1}");
  myText(0.18,0.77,1,"Powheg Z#rightarrow ee");

  TCanvas c3("c3","c3",600,600);
  //c3.SetLogy();
  c3.SetLogx();
  hSSCHF1Clone->Draw("ep0");
  hSSCHF1Clone->GetYaxis()->SetRangeUser(0,2);
  hSSCHF1Clone->GetYaxis()->SetTitle("CHF type-2 / CHF type-4");
  hSSCHF1Clone->GetXaxis()->SetTitle("m(e^{#pm}e^{#pm})");
  hSSCHF1Clone->GetXaxis()->SetNoExponent();
  hSSCHF1Clone->GetXaxis()->SetMoreLogLabels();
  ATLASLabel(0.18,0.88,"internal",1);
  myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 36.5 fb^{-1}");
  myText(0.18,0.77,1,"Powheg Z#rightarrow ee");

  TCanvas c4("c4","c4",600,600);
  std::vector<TH1D*> h1vec;
  h1vec.push_back( ((TH1D*)hCHFr) );
  h1vec.push_back( ((TH1D*)hBothCHFr) );
  h1vec.push_back( ((TH1D*)hBothCHFSFr) );
  drawComparison2(&c4,&h1vec,(TH1D*)hCHFSFr,"probability [%]","m(e^{#pm}e^{#pm})",0,25,130,7000,true,0.7,1.3);
  ATLASLabel(0.18,0.83,"internal",1);
  myText(0.18,0.78,1,"#sqrt{s} = 13 TeV, 36.5 fb^{-1}");
  myText(0.18,0.72,1,"Powheg Z#rightarrow ee");
  leg2->Draw();
  //gROOT->ProcessLine("pad_1->SetLogy();");

  //hSSCHF1Clone->GetXaxis()->SetRangeUser(50,130);

  int xbins = hCHF130M300->GetNbinsX();
  for (int eta = 1; eta < hCHF130M300->GetNbinsY(); eta++){
    hCHF130M300->SetBinContent( xbins, eta, hCHF130M300->GetBinContent(xbins, eta) + hCHF130M300->GetBinContent(xbins+1, eta)  );
    hCHF300M1200->SetBinContent( xbins, eta, hCHF300M1200->GetBinContent(xbins, eta) + hCHF300M1200->GetBinContent(xbins+1, eta)  );
    hCHFM1200->SetBinContent( xbins, eta, hCHFM1200->GetBinContent(xbins, eta) + hCHFM1200->GetBinContent(xbins+1, eta)  );
  }

  gStyle->SetPaintTextFormat("3.0f");

  TCanvas c5("c5","c5",800,600);
  c5.SetLogx();
  c5.SetRightMargin(0.2);
  c5.SetLeftMargin(0.12);
  hCHF130M300->Scale(100./hCHF130M300->Integral());
  hCHF130M300->Draw("colz text");
  hCHF130M300->GetYaxis()->SetTitle("abs(#eta)");
  hCHF130M300->GetYaxis()->SetTitleOffset(1.0);
  hCHF130M300->GetXaxis()->SetTitle("p_{T} [GeV]");
  hCHF130M300->GetXaxis()->SetNoExponent();
  hCHF130M300->GetXaxis()->SetMoreLogLabels();
  hCHF130M300->GetZaxis()->SetTitle("Normalized Entries [%]");
  hCHF130M300->GetZaxis()->SetTitleOffset(1.5);
  myText(0.18,0.9,1,"charge-flipped electrons");
  myText(0.18,0.85,1,"130 GeV < m(e^{#pm}e^{#pm}) < 300 GeV");

  TCanvas c6("c6","c6",800,600);
  c6.SetLogx();
  c6.SetRightMargin(0.2);
  c6.SetLeftMargin(0.12);
  hCHF300M1200->Scale(100./hCHF300M1200->Integral());
  hCHF300M1200->Draw("colz text");
  hCHF300M1200->GetYaxis()->SetTitle("abs(#eta)");
  hCHF300M1200->GetYaxis()->SetTitleOffset(1.0);
  hCHF300M1200->GetXaxis()->SetTitle("p_{T} [GeV]");
  hCHF300M1200->GetXaxis()->SetNoExponent();
  hCHF300M1200->GetXaxis()->SetMoreLogLabels();
  hCHF300M1200->GetZaxis()->SetTitle("Normalized Entries [%]");
  hCHF300M1200->GetZaxis()->SetTitleOffset(1.5);
  myText(0.18,0.9,1,"charge-flipped electrons");
  myText(0.18,0.85,1,"300 GeV < m(e^{#pm}e^{#pm}) < 1200 GeV");

  TCanvas c7("c7","c7",800,600);
  c7.SetLogx();
  c7.SetRightMargin(0.2);
  c7.SetLeftMargin(0.12);
  hCHFM1200->Scale(100./hCHFM1200->Integral());
  hCHFM1200->Draw("colz text");
  hCHFM1200->GetYaxis()->SetTitle("abs(#eta)");
  hCHFM1200->GetYaxis()->SetTitleOffset(1.0);
  hCHFM1200->GetXaxis()->SetTitle("p_{T} [GeV]");
  hCHFM1200->GetXaxis()->SetNoExponent();
  hCHFM1200->GetXaxis()->SetMoreLogLabels();
  hCHFM1200->GetZaxis()->SetTitle("Normalized Entries [%]");
  hCHFM1200->GetZaxis()->SetTitleOffset(1.5);
  myText(0.18,0.9,1,"charge-flipped electrons");
  myText(0.18,0.85,1,"1200 GeV < m(e^{#pm}e^{#pm})");
  // ATLASLabel(0.18,0.88,"internal",1);
  // myText(0.18,0.82,1,"#sqrt{s} = 13 TeV, 36.5 fb^{-1}");
  // myText(0.18,0.77,1,"Powheg Z#rightarrow ee");


  c1.Print("cOS-CHF1.eps");
  c2.Print("cSS-CHF1.eps");
  c3.Print("cRatio-CHF1.eps");
  c4.Print("cCHF.eps");
  c5.Print("cCHF130M300.eps");
  c6.Print("cCHF300M1200.eps");
  c7.Print("cCHF1200M.eps");



}