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


//-------------------------------------------------
// Numerical Minimizer Class ----------------------
//-------------------------------------------------
class NumericalMinimizer {

public:
  NumericalMinimizer();
  NumericalMinimizer(TH1F* hOSCenter=nullptr, TH1F* hSSCenter=nullptr, TH1F* hOSSideband=nullptr, TH1F* hSSSideband=nullptr);

  TH1F* m_hOSCenter;
  TH1F* m_hSSCenter;
  TH1F* m_hOSSideband;
  TH1F* m_hSSSideband;

  double m_ptBins[12] = {30., 40., 50., 60., 70., 80., 90., 100., 125., 150., 200.,400.};
  //double m_etaBins[10] = {0.0, 0.75, 1.1, 1.37, 1.52, 1.7, 1.9, 2.1, 2.3, 2.5};
  //double m_etaBins[18] = {0.0, 0.25, 0.50, 0.75, 1.0, 1.20, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};
  double m_etaBins[16] = {0.0, 0.50, 1.0, 1.20, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};

  int m_NetaBins;
  int m_NptBins;

  ROOT::Math::Minimizer* m_min = nullptr;
  TH1D* m_flipRatePt = nullptr;
  TH1D* m_flipRateEta = nullptr;

  TFile* m_outFile = nullptr;

  ROOT::Math::Minimizer* NumericalMinimization1D(const char* minName = "Minuit2", const char* algoName = "" , int randomSeed = -1);
  double LogLikelihood1D(const double*);

};

NumericalMinimizer::NumericalMinimizer (TH1F* hOSCenter, TH1F* hSSCenter, TH1F* hOSSideband, TH1F* hSSSideband):
m_hOSCenter(hOSCenter),
m_hSSCenter(hSSCenter),
m_hOSSideband(hOSSideband),
m_hSSSideband(hSSSideband)
{
  std::string xTitle = std::string( m_hOSCenter->GetXaxis()->GetTitle() );
  std::stringstream ss(xTitle);
  std::string tempStr;
  ss >> tempStr >> m_NptBins >> tempStr >> m_NetaBins;
  std::cout << "NetaBins: " << m_NetaBins << " NptBins: " << m_NptBins << std::endl;
  if(m_hOSCenter->GetNbinsX()!=m_NetaBins*m_NetaBins*m_NptBins*m_NptBins){
    std::cout << "error: bins don't match" << std::endl;
  }
  else{
    std::cout << "number of bins seem to match the total number of bins: " << m_hOSCenter->GetNbinsX() << std::endl;
  }

  if(m_hOSSideband) {
    std::cout << "subtracting the OS sideband.." << std::endl;
    m_hOSCenter->Add(m_hOSSideband,-1);
  }
  if(m_hSSSideband) {
    std::cout << "subtracting the SS sideband.." << std::endl;
    m_hSSCenter->Add(m_hSSSideband,-1);
  }

  m_min = NumericalMinimization1D();
  ROOT::Fit::ParameterSettings pars;
  m_flipRatePt =  new TH1D( (std::string("flipRatePt")+hOSCenter->GetTitle()).c_str(), (std::string("flipRatePt")+hOSCenter->GetTitle()).c_str(), m_NptBins, &m_ptBins[0] );
  m_flipRateEta = new TH1D( (std::string("flipRateEta")+hOSCenter->GetTitle()).c_str(), (std::string("flipRateEta")+hOSCenter->GetTitle()).c_str(), m_NetaBins, &m_etaBins[0] );
  for (int eta = 0; eta < m_NetaBins; eta++){
    m_min->GetVariableSettings( eta, pars );
    if (m_etaBins[eta] >= 1.37 && m_etaBins[eta] < 1.52) {
      m_flipRateEta->SetBinContent(eta+1,0);
      m_flipRateEta->SetBinError(eta+1,0);      
    }
    else{
      m_flipRateEta->SetBinContent(eta+1,pars.Value());
      m_flipRateEta->SetBinError(eta+1,pars.StepSize());
    }
  }
  for (int pt = 0; pt < m_NptBins; pt++) {
    m_min->GetVariableSettings( m_NetaBins+pt, pars );
    m_flipRatePt->SetBinContent(pt+1,pars.Value());
    m_flipRatePt->SetBinError(pt+1,pars.StepSize());
  }

  m_outFile = new TFile( (std::string("chargeFlipRates_")+hOSCenter->GetTitle()+std::string(".root")).c_str(), "RECREATE" );
  m_flipRatePt->Write();
  m_flipRateEta->Write();
  m_outFile->Close();
}

//-------------------------------------------------
// ROOT::Math::Minimizer --------------------------
//-------------------------------------------------
ROOT::Math::Minimizer* NumericalMinimizer::NumericalMinimization1D(const char * minName,
                          const char *algoName,
                          int randomSeed )
{
 ROOT::Math::Minimizer* min =
 ROOT::Math::Factory::CreateMinimizer(minName, algoName);

   min->SetMaxFunctionCalls(1e7); // for Minuit/Minuit2
   min->SetMaxIterations(1e5);  // for GSL
   min->SetTolerance(1e-5);
   min->SetPrintLevel(1);

   auto func = &NumericalMinimizer::LogLikelihood1D;
   ROOT::Math::Functor f(this,func,m_NetaBins+m_NptBins);

   min->SetFunction(f);

   int index = 0;
   double stepSize = 1e-5;
   for (int eta = 1; eta <= m_NetaBins; eta++){
    std::ostringstream name;
    name << "eta" << eta;
    min->SetVariable(index,name.str().c_str(),0,stepSize);
    min->SetVariableLowerLimit(index,stepSize);
    index++;
  }
  for (int pt = 1; pt <= m_NptBins; pt++){
    std::ostringstream name;
    name << "pt" << pt;
    min->SetVariable(index,name.str().c_str(),0,stepSize);
    min->SetVariableLowerLimit(index,stepSize);
    index++;
  }

  min->Minimize();

  return min;
}

//-------------------------------------------------
// Log Likelihood    1Dx1D   ----------------------
//-------------------------------------------------
double NumericalMinimizer::LogLikelihood1D(const double *xx )
{
  double value = 1e2;
  for(int pt1 = 1; pt1 <= m_NptBins; pt1++) {
    for(int eta1 = 1; eta1 <= m_NetaBins; eta1++) {
      for(int pt2 = 1; pt2 <= m_NptBins; pt2++) {
        for(int eta2 = 1; eta2 <= m_NetaBins; eta2++){
          // totBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          int totBin = ( (pt1-1)*m_NetaBins + eta1 - 1 )*m_NptBins*m_NetaBins + ( (pt2-1)*m_NetaBins + eta2 ) + 1;
          value += -m_hSSCenter->GetBinContent(totBin) * log (xx[eta1-1]*xx[m_NetaBins+pt1-1] + xx[eta2-1]*xx[m_NetaBins+pt2-1] ) 
          + m_hOSCenter->GetBinContent(totBin)*( xx[eta1-1]*xx[m_NetaBins+pt1-1] + xx[eta2-1]*xx[m_NetaBins+pt2-1]  );
        }
      }
    }
  }
  double etaNorm = 0;
  for(int eta1 = 0; eta1 < m_NetaBins; eta1++) {
    if (m_etaBins[eta1] >= 1.37 && m_etaBins[eta1] < 1.52) continue;
    etaNorm += (m_etaBins[eta1+1]-m_etaBins[eta1])*xx[eta1];
  }
  return value + 1e8*pow((etaNorm-1),2);
}

void charge_flip_measurement(){

  /*std::string OSCenterInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowOS_Powheg.root";
  std::string OSSidebandInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowOS-Sideband_Powheg.root";
  std::string SSCenterInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowSS_Powheg.root";
  std::string SSSidebandInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";
  */
  std::string OSCenterInputFile = "/ceph/grid/home/atlas/miham/storage/Plots.15.Nov/hists_chargeFlipHist_ZWindowOS_Powheg.root";
  std::string OSSidebandInputFile = "/ceph/grid/home/atlas/miham/storage/Plots.15.Nov/hists_chargeFlipHist_ZWindowOS-Sideband_Powheg.root";
  std::string SSCenterInputFile = "/ceph/grid/home/atlas/miham/storage/Plots.15.Nov/hists_chargeFlipHist_ZWindowSS_Powheg.root";
  std::string SSSidebandInputFile = "/ceph/grid/home/atlas/miham/storage/Plots.15.Nov/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";
  

  TFile* OSCenterFile   = new TFile(OSCenterInputFile.c_str());
  TFile* OSSidebandFile = new TFile(OSSidebandInputFile.c_str());
  TFile* SSCenterFile   = new TFile(SSCenterInputFile.c_str());
  TFile* SSSidebandFile = new TFile(SSSidebandInputFile.c_str());

  TH1F* hOSCenterData = (TH1F*) OSCenterFile->Get("h_ZWindowOS_nominal_data");
  TH1F* hOSCenterMC   = (TH1F*) OSCenterFile->Get("h_ZWindowOS_nominal_Zee");
  TH1F* hSSCenterData = (TH1F*) SSCenterFile->Get("h_ZWindowSS_nominal_data");
  TH1F* hSSCenterMC   = (TH1F*) SSCenterFile->Get("h_ZWindowSS_nominal_Zee");
  TH1F* hOSSidebandData = (TH1F*) OSSidebandFile->Get("h_ZWindowOS-Sideband_nominal_data");
  TH1F* hOSSidebandMC   = (TH1F*) OSSidebandFile->Get("h_ZWindowOS-Sideband_nominal_Zee");
  TH1F* hSSSidebandData = (TH1F*) SSSidebandFile->Get("h_ZWindowSS-Sideband_nominal_data");
  TH1F* hSSSidebandMC   = (TH1F*) SSSidebandFile->Get("h_ZWindowSS-Sideband_nominal_Zee");

  if(hOSCenterData) std::cout << "h_ZWindowOS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_data not found" <<std::endl;
  if(hOSCenterMC) std::cout << "h_ZWindowOS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_Zee not found" <<std::endl;
  if(hSSCenterData) std::cout << "h_ZWindowSS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_data not found" <<std::endl;
  if(hSSCenterMC) std::cout << "h_ZWindowSS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_Zee not found" <<std::endl;
  if(hOSSidebandData) std::cout << "h_ZWindowOS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_data not found" <<std::endl;
  if(hOSSidebandMC) std::cout << "h_ZWindowOS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_Zee not found" <<std::endl;
  if(hSSSidebandData) std::cout << "h_ZWindowSS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_data not found" <<std::endl;
  if(hSSSidebandMC) std::cout << "h_ZWindowSS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_Zee not found" <<std::endl;

  hOSCenterData->Add(hSSCenterData);
  hOSSidebandData->Add(hSSSidebandData);

  std::cout << " data charge-flip measurement " << std::endl;
  NumericalMinimizer NM1(hOSCenterData,hSSCenterData,hOSSidebandData,hSSSidebandData);
  std::cout << " MC charge-flip measurement " << std::endl;
  NumericalMinimizer NM2(hOSCenterMC,hSSCenterMC,hOSSidebandMC,hSSSidebandMC);

  std::cout << " start drawing " << std::endl;
  NM2.m_flipRateEta->SetLineColor(kRed);
  NM2.m_flipRateEta->SetMarkerColor(kRed);
  NM2.m_flipRatePt->SetLineColor(kRed);
  NM2.m_flipRatePt->SetMarkerColor(kRed);

  // legend
  TLegend* leg = new TLegend(0.20,0.600,0.4,0.725);
  leg->SetBorderSize(0);
  leg->SetFillColor(0);
  leg->SetFillStyle(0);
  leg->SetTextSize(0.045);
  leg->AddEntry(NM1.m_flipRateEta,"#font[42]{Data}","lpe0");
  leg->AddEntry(NM2.m_flipRateEta,"#font[42]{Sherpa 2.21 Z#rightarrow ee}","lpe0");

  TCanvas* c1 = new TCanvas("c1","c1",600,600);
  c1->cd();
  drawComparison2(c1,NM2.m_flipRateEta,NM1.m_flipRateEta,"f(#eta)","#eta",1e-2,10,0,2.47);
  ATLASLabel(0.20,0.83,"internal",1);
  myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}");
  myText(0.60,0.75,1,"P_{CHF}(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();
  gROOT->ProcessLine("pad_1->SetLogy();");
  //c1->SetLogy();
  /*NM1.m_flipRateEta->Draw();
  NM1.m_flipRateEta->GetXaxis()->SetTitle("#eta");
  NM1.m_flipRateEta->GetYaxis()->SetTitle("f(#eta)");
  NM1.m_flipRateEta->GetYaxis()->SetRangeUser(1e-2,2);
  NM2.m_flipRateEta->Draw("same");
  NM2.m_flipRateEta->SetLineColor(kRed);
  NM2.m_flipRateEta->SetMarkerColor(kRed);*/
  //ATLAS_LABEL(0.20,0.88,1); myText(0.35,0.9,1,"internal",0.055);
  //myText(0.20,0.84,1,"#sqrt{s} = 13 TeV, 13.9 fb^{-1}",0.055);

  TCanvas* c2 = new TCanvas("c2","c2",600,600);
  c2->cd();
  histo_overUnderFlow(NM2.m_flipRatePt);
  histo_overUnderFlow(NM1.m_flipRatePt);
  drawComparison2(c2,NM2.m_flipRatePt,NM1.m_flipRatePt,"#sigma(p_{T})","p_{T} [GeV]",0,0.2,30,400,true);
  ATLASLabel(0.20,0.83,"internal",1);
  myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 18.2 fb^{-1}");
  myText(0.60,0.75,1,"P_{CHF}(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();
  //c2->SetLogy();
  /*c2->SetLogx();
  NM1.m_flipRatePt->Draw();
  NM1.m_flipRatePt->GetXaxis()->SetTitle("p_{T} [GeV]");
  NM1.m_flipRatePt->GetYaxis()->SetTitle("#sigma(p_{T})");
  NM1.m_flipRatePt->GetYaxis()->SetRangeUser(1e-2,0.2);
  NM2.m_flipRatePt->Draw("same");
  NM2.m_flipRatePt->SetLineColor(kRed);
  NM2.m_flipRatePt->SetMarkerColor(kRed);*/
  //ATLAS_LABEL(0.20,0.88,1); myText(0.35,0.9,1,"internal",0.055);
  //myText(0.20,0.84,1,"#sqrt{s} = 13 TeV, 13.9 fb^{-1}",0.055);

  c1->Print("chargeFlipEta.eps");
  c2->Print("chargeFlipPt.eps");

}