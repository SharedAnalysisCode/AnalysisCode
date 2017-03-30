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

void charge_flip_wifth_fit(){

  TFile* ZeeAS   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_invMassPeak_ZWindowAS_CF.root");
  TFile* ZeeSS   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_invMassPeak_ZWindowSS_CF.root");

  TH1D* hZeeAS = (TH1D*) ZeeAS->Get("h_ZWindowAS_nominal_data");
  TH1D* hZeeSS = (TH1D*) ZeeSS->Get("h_ZWindowSS_nominal_data");

  
}