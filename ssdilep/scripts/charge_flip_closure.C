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

void charge_flip_closure(){
  
  TFile* el_all = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_pt_eta_ZWindowSS_CF.root");
  TFile* el_lead = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_lead_pt_eta_ZWindowSS_CF.root");
  TFile* el_sublead = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_sublead_pt_eta_ZWindowSS_CF.root");

  TFile* el_all_MC_SS = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_pt_eta_ZWindowSS_CFMC.root");
  TFile* el_lead_MC_SS = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_lead_pt_eta_ZWindowSS_CFMC.root");
  TFile* el_sublead_MC_SS = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_sublead_pt_eta_ZWindowSS_CFMC.root");

  TFile* el_all_MC_OS = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_pt_eta_ZWindowOStoSS_CFMC.root");
  TFile* el_lead_MC_OS = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_lead_pt_eta_ZWindowOStoSS_CFMC.root");
  TFile* el_sublead_MC_OS = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_el_sublead_pt_eta_ZWindowOStoSS_CFMC.root");

  TFile* chargeFlipRate = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/chargeFlipRate.root");
  TH1D* dataPtRate  = (TH1D*) chargeFlipRate->Get("dataPtRate");
  TH1D* dataEtaRate = (TH1D*) chargeFlipRate->Get("dataEtaRate");
  TH1D* MCPtRate  = (TH1D*) chargeFlipRate->Get("MCPtRate");
  TH1D* MCEtaRate = (TH1D*) chargeFlipRate->Get("MCEtaRate");

  TH2D* hel_all_data = (TH2D*) el_all->Get("h_ZWindowSS_nominal_data");
  TH2D* hel_all_chfb = (TH2D*) el_all->Get("h_ZWindowSS_nominal_chargeFlip");
  TH2D* hel_all_chfb_UP = (TH2D*) el_all->Get("h_ZWindowSS_CF_UP_chargeFlip");
  TH2D* hel_all_chfb_DN = (TH2D*) el_all->Get("h_ZWindowSS_CF_DN_chargeFlip");

  TH2D* hel_all_data_MC = (TH2D*) el_all_MC_SS->Get("h_ZWindowSS_nominal_Zee221");
  TH2D* hel_all_chfb_MC = (TH2D*) el_all_MC_OS->Get("h_ZWindowOStoSS_nominal_Zee221");
  TH2D* hel_all_chfb_MC_UP = (TH2D*) el_all_MC_OS->Get("h_ZWindowOStoSS_CF_UP_Zee221");
  TH2D* hel_all_chfb_MC_DN = (TH2D*) el_all_MC_OS->Get("h_ZWindowOStoSS_CF_DN_Zee221");

  for (int i = 1; i <= hel_all_data->GetNbinsX()+1; i++){
    TH1D* dataSlice = hel_all_data->ProjectionY(Form("dataSliceY%d",i),i,i);
    TH1D* chfbSlice = hel_all_chfb->ProjectionY(Form("chfbSliceY%d",i),i,i);
    TH1D* chfbSlice_UP = hel_all_chfb_UP->ProjectionY(Form("chfbSliceUPY%d",i),i,i);
    TH1D* chfbSlice_DN = hel_all_chfb_DN->ProjectionY(Form("chfbSliceDNY%d",i),i,i);

    TGraphAsymmErrors* sysBandSlice = myMakeBand_2(TH1TOTGraph_2(chfbSlice), TH1TOTGraph_2(chfbSlice_DN) ,TH1TOTGraph_2(chfbSlice_UP) );
    sysBandSlice->SetFillColor(kYellow);
    sysBandSlice->SetLineColor(kYellow);

    chfbSlice->SetLineColor(kRed);
    chfbSlice->SetMarkerColor(kRed);
    std::vector<TH1D*> c1h1vec;
    c1h1vec.push_back(chfbSlice);
    TCanvas c1("c1","c1",600,600);
    drawComparison2(&c1,&c1h1vec,dataSlice,"Events","abs(#eta)",0,2.5*dataSlice->GetMaximum(),0,2.5,false,0.4,1.6,true,0,false,"PE0",false,sysBandSlice);
    ATLASLabel(0.20,0.83,"internal",1);
    myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.5 fb^{-1}");
    double rightEdge = i!=hel_all_data->GetNbinsX()+1 ? hel_all_data->GetXaxis()->GetBinLowEdge(i)+hel_all_data->GetXaxis()->GetBinWidth(i) : std::numeric_limits<double>::infinity();
    myText(0.18,0.67,1,Form("%4.0f GeV < pt < %4.0f GeV",hel_all_data->GetXaxis()->GetBinLowEdge(i),rightEdge));
    myText(0.60,0.83,1,"charge-flip closure");

    TLegend* leg = new TLegend(0.60,0.64,0.925,0.8);
    leg->SetBorderSize(0);
    leg->SetFillColor(0);
    leg->SetFillStyle(0);
    leg->SetTextSize(0.045);
    leg->AddEntry(dataSlice,"#font[42]{SS Data}","lpe0");
    leg->AddEntry(chfbSlice,"#font[42]{OS Data * CF}","lpe0");
    leg->AddEntry(sysBandSlice,"#font[42]{CF sys (LH fit)}","f");
    leg->Draw();

    c1.Print(Form("chargeFlipClosure_slice%d.eps",i));
    if (i!=hel_all_data->GetNbinsX()+1)
      c1.Print(Form("chargeFlipClosureSlices.pdf("));
    else
      c1.Print(Form("chargeFlipClosureSlices.pdf)"));
  }

  for (int i = 1; i <= hel_all_data->GetNbinsX()+1; i++){
    TH1D* dataSlice = hel_all_data_MC->ProjectionY(Form("dataSliceYMC%d",i),i,i);
    TH1D* chfbSlice = hel_all_chfb_MC->ProjectionY(Form("chfbSliceYMC%d",i),i,i);
    TH1D* chfbSlice_UP = hel_all_chfb_MC_UP->ProjectionY(Form("chfbSliceUPYMC%d",i),i,i);
    TH1D* chfbSlice_DN = hel_all_chfb_MC_DN->ProjectionY(Form("chfbSliceDNYMC%d",i),i,i);

    TGraphAsymmErrors* sysBandSlice = myMakeBand_2(TH1TOTGraph_2(chfbSlice), TH1TOTGraph_2(chfbSlice_DN) ,TH1TOTGraph_2(chfbSlice_UP) );
    sysBandSlice->SetFillColor(kYellow);
    sysBandSlice->SetLineColor(kYellow);

    chfbSlice->SetLineColor(kRed);
    chfbSlice->SetMarkerColor(kRed);
    std::vector<TH1D*> c1h1vec;
    c1h1vec.push_back(chfbSlice);
    TCanvas c1("c1","c1",600,600);
    drawComparison2(&c1,&c1h1vec,dataSlice,"Events","abs(#eta)",0,2.5*dataSlice->GetMaximum(),0,2.5,false,0.4,1.6,true,0,false,"PE0",false,sysBandSlice);
    ATLASLabel(0.20,0.83,"internal",1);
    myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, Zee Sherpa 2.21");
    double rightEdge = i!=hel_all_data->GetNbinsX()+1 ? hel_all_data->GetXaxis()->GetBinLowEdge(i)+hel_all_data->GetXaxis()->GetBinWidth(i) : std::numeric_limits<double>::infinity();
    myText(0.18,0.67,1,Form("%4.0f GeV < pt < %4.0f GeV",hel_all_data->GetXaxis()->GetBinLowEdge(i),rightEdge));
    myText(0.60,0.83,1,"charge-flip closure");

    TLegend* leg = new TLegend(0.60,0.64,0.925,0.8);
    leg->SetBorderSize(0);
    leg->SetFillColor(0);
    leg->SetFillStyle(0);
    leg->SetTextSize(0.045);
    leg->AddEntry(dataSlice,"#font[42]{SS MC(Zee)}","lpe0");
    leg->AddEntry(chfbSlice,"#font[42]{OS MC(Zee) * CF}","lpe0");
    leg->AddEntry(sysBandSlice,"#font[42]{CF sys (LH fit)}","f");
    leg->Draw();

    c1.Print(Form("chargeFlipClosure_MC_slice%d.eps",i));
    if (i!=hel_all_data->GetNbinsX()+1)
      c1.Print(Form("chargeFlipClosureSlices_MC.pdf("));
    else
      c1.Print(Form("chargeFlipClosureSlices_MC.pdf)"));
  }
  
}