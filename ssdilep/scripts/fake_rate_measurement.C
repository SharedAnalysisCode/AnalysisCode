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
  
  TFile* nominal_t   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/Plots/hists_el_t_2D_pt_eta_FakeEnrichedRegion-nominal_FFnominal.root");
  TFile* nominal_l   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/Plots/hists_el_l_2D_pt_eta_FakeEnrichedRegion-nominal_FFnominal.root");
  TFile* nominal_sl   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/Plots/hists_el_sl_2D_pt_eta_FakeEnrichedRegion-nominal_FFnominal.root");

  TH2F* nominal_t_wenu = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_WenuPowheg");
  TH2F* nominal_t_zee = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_Zee221");
  TH2F* nominal_t_ttbar = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_ttbar_dilep");
  TH2F* nominal_t_diboson = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_diboson_sherpa");
  TH2F* nominal_t_data = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_data");

  TH2F* nominal_l_wenu = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_WenuPowheg");
  TH2F* nominal_l_zee = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_Zee221");
  TH2F* nominal_l_ttbar = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_ttbar_dilep");
  TH2F* nominal_l_diboson = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_diboson_sherpa");
  TH2F* nominal_l_data = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_data");

  TH2F* nominal_sl_wenu = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_WenuPowheg");
  TH2F* nominal_sl_zee = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_Zee221");
  TH2F* nominal_sl_ttbar = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_ttbar_dilep");
  TH2F* nominal_sl_diboson = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_diboson_sherpa");
  TH2F* nominal_sl_data = (TH2F*) AllElePow->Get("h_FakeEnrichedRegion-nominal_nominal_data");



  
}