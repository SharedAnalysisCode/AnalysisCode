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
  NumericalMinimizer(TH1F* hOSCenter=nullptr, TH1F* hSSCenter=nullptr, TH1F* hOSSideband=nullptr, TH1F* hSSSideband=nullptr, double aa=1e9);

  TH1F* m_hOSCenter;
  TH1F* m_hSSCenter;
  TH1F* m_hOSSideband;
  TH1F* m_hSSSideband;

  // double m_ptBins[14] = {30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 140., 200., 400.};
  // double m_etaBins[17] = {0.0, 0.3, 0.50, 1.0, 1.20, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};
  double m_ptBins[15] = {30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200., 400.};
  double m_etaBins[19] = {0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};

  const double m_constraint = 1e9;

  int m_NetaBins;
  int m_NptBins;

  ROOT::Math::Minimizer* m_min = nullptr;
  TH1D* m_flipRatePt = nullptr;
  TH1D* m_flipRateEta = nullptr;

  TFile* m_outFile = nullptr;

  ROOT::Math::Minimizer* NumericalMinimization1D(const char* minName = "Minuit2", const char* algoName = "" , int randomSeed = -1);
  double LogLikelihood1D(const double*);
  double LogLikelihood1Dfull(const double*);

};

NumericalMinimizer::NumericalMinimizer (TH1F* hOSCenter, TH1F* hSSCenter, TH1F* hOSSideband, TH1F* hSSSideband, double aa):
m_hOSCenter(hOSCenter),
m_hSSCenter(hSSCenter),
m_hOSSideband(hOSSideband),
m_hSSSideband(hSSSideband),
m_constraint(aa)
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

  m_flipRatePt->GetXaxis()->SetRangeUser(m_ptBins[0],m_ptBins[m_NptBins+1]);

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

   min->SetMaxFunctionCalls(1e9); // for Minuit/Minuit2
   min->SetMaxIterations(1e9);  // for GSL
   min->SetTolerance(1e-6);
   min->SetPrintLevel(1);

   auto func = &NumericalMinimizer::LogLikelihood1Dfull;
   ROOT::Math::Functor f(this,func,m_NetaBins+m_NptBins);

   min->SetFunction(f);

   int index = 0;
   double stepSize = 1e-6;
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
// Log Likelihood    1Dx1D   approximation
//-------------------------------------------------
double NumericalMinimizer::LogLikelihood1D(const double *xx )
{
  double value = 0;
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
  return value + m_constraint*pow((etaNorm-1),2);
}

//-------------------------------------------------
// Log Likelihood    1Dx1D   full formula
//-------------------------------------------------
double NumericalMinimizer::LogLikelihood1Dfull(const double *xx )
{
  double value = 0;
  for(int pt1 = 1; pt1 <= m_NptBins; pt1++) {
    for(int eta1 = 1; eta1 <= m_NetaBins; eta1++) {
      for(int pt2 = 1; pt2 <= m_NptBins; pt2++) {
        for(int eta2 = 1; eta2 <= m_NetaBins; eta2++){
          // totBin = ( (ptbin1-1)*(len(eta_bins)-1) + etabin1-1 )*(len(eta_bins)-1)*len(pt_bins) + ( (ptbin2-1)*(len(eta_bins)-1) + etabin2 )
          int totBin = ( (pt1-1)*m_NetaBins + eta1 - 1 )*m_NptBins*m_NetaBins + ( (pt2-1)*m_NetaBins + eta2 ) + 1;
          value += -m_hSSCenter->GetBinContent(totBin) * log( xx[eta1-1]*xx[m_NetaBins+pt1-1]*(1-xx[eta2-1]*xx[m_NetaBins+pt2-1]) + 
                                                              xx[eta2-1]*xx[m_NetaBins+pt2-1]*(1-xx[eta1-1]*xx[m_NetaBins+pt1-1]) ) 
          + m_hOSCenter->GetBinContent(totBin)*( xx[eta1-1]*xx[m_NetaBins+pt1-1]*(1-xx[eta2-1]*xx[m_NetaBins+pt2-1]) + 
                                                 xx[eta2-1]*xx[m_NetaBins+pt2-1]*(1-xx[eta1-1]*xx[m_NetaBins+pt1-1]) );
        }
      }
    }
  }
  double etaNorm = 0;
  for(int eta1 = 0; eta1 < m_NetaBins; eta1++) {
    if (m_etaBins[eta1] >= 1.37 && m_etaBins[eta1] < 1.52) continue;
    etaNorm += (m_etaBins[eta1+1]-m_etaBins[eta1])*xx[eta1];
  }
  return value + m_constraint*pow((etaNorm-1),2);
}

void charge_flip_measurement(){

  // 27. feb 2017 with
  // pt_bins  = [30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 140., 200.] # last pt bin is open
  // eta_bins = [0.0, 0.30, 0.50, 1.0, 1.20, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
  // std::string OSCenterInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_27_Feb/hists_chargeFlipHist_ZWindowAS_Powheg.root";
  // std::string OSSidebandInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_27_Feb/hists_chargeFlipHist_ZWindowAS-Sideband_Powheg.root";
  // std::string SSCenterInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_27_Feb/hists_chargeFlipHist_ZWindowSS_Powheg.root";
  // std::string SSSidebandInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_27_Feb/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";

  // 01. mar 2017 with
  // double m_ptBins[15] = {30., 34., 38., 43., 48., 55., 62., 69., 78.0, 88.0, 100., 115., 140., 200., 400.};
  // double m_etaBins[19] = {0.0, 0.45, 0.7, 0.9, 1.0, 1.1, 1.2, 1.37, 1.52, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5};
  //    min->SetTolerance(1e-6); double stepSize = 1e-6; ,1e6); ,1e6);
  // std::string OSCenterInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_01_Mar/hists_chargeFlipHist_ZWindowAS_Powheg.root";
  // std::string OSSidebandInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_01_Mar/hists_chargeFlipHist_ZWindowAS-Sideband_Powheg.root";
  // std::string SSCenterInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_01_Mar/hists_chargeFlipHist_ZWindowSS_Powheg.root";
  // std::string SSSidebandInputFile = "/ceph/grid/home/atlas/miham/storage/ZPeak36_01_Mar/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";

  // std::string OSCenterInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_v3_002_cf/hists_chargeFlipHist_ZWindowAS_Powheg.root";
  // std::string OSSidebandInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_v3_002_cf/hists_chargeFlipHist_ZWindowAS-Sideband_Powheg.root";
  // std::string SSCenterInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_v3_002_cf/hists_chargeFlipHist_ZWindowSS_Powheg.root";
  // std::string SSSidebandInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_v3_002_cf/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";
  
  std::string OSCenterInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_HN_chargeflip_001/hists_chargeFlipHist_ZWindowAS_Powheg.root";
  std::string OSSidebandInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_HN_chargeflip_001/hists_chargeFlipHist_ZWindowAS-Sideband_Powheg.root";
  std::string SSCenterInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_HN_chargeflip_001/hists_chargeFlipHist_ZWindowSS_Powheg.root";
  std::string SSSidebandInputFile = "/afs/f9.ijs.si/home/miham/AnalysisCode/run/ZPeak_HN_chargeflip_001/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";
  
  

  TFile* OSCenterFile   = new TFile(OSCenterInputFile.c_str());
  TFile* OSSidebandFile = new TFile(OSSidebandInputFile.c_str());
  TFile* SSCenterFile   = new TFile(SSCenterInputFile.c_str());
  TFile* SSSidebandFile = new TFile(SSSidebandInputFile.c_str());

  TH1F* hOSCenterData = (TH1F*) OSCenterFile->Get("h_ZWindowAS_nominal_full_2015-2016_physics_Main");
  TH1F* hOSCenterMC   = (TH1F*) OSCenterFile->Get("h_ZWindowAS_nominal_Zee221");
  TH1F* hSSCenterData = (TH1F*) SSCenterFile->Get("h_ZWindowSS_nominal_full_2015-2016_physics_Main");
  TH1F* hSSCenterMC   = (TH1F*) SSCenterFile->Get("h_ZWindowSS_nominal_Zee221");
  TH1F* hOSSidebandData = (TH1F*) OSSidebandFile->Get("h_ZWindowAS-Sideband_nominal_full_2015-2016_physics_Main");
  TH1F* hOSSidebandMC   = (TH1F*) OSSidebandFile->Get("h_ZWindowAS-Sideband_nominal_Zee221");
  TH1F* hSSSidebandData = (TH1F*) SSSidebandFile->Get("h_ZWindowSS-Sideband_nominal_full_2015-2016_physics_Main");
  TH1F* hSSSidebandMC   = (TH1F*) SSSidebandFile->Get("h_ZWindowSS-Sideband_nominal_Zee221");

  if(hOSCenterData) std::cout << "h_ZWindowOS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_data not found" <<std::endl;
  if(hOSCenterMC) std::cout << "h_ZWindowOS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS_nominal_Zee not found" <<std::endl;
  if(hSSCenterData) std::cout << "h_ZWindowSS_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_data not found" <<std::endl;
  if(hSSCenterMC) std::cout << "h_ZWindowSS_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS_nominal_Zee not found" <<std::endl;
  if(hOSSidebandData) std::cout << "h_ZWindowOS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_data not found" <<std::endl;
  if(hOSSidebandMC) std::cout << "h_ZWindowOS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowOS-Sideband_nominal_Zee not found" <<std::endl;
  if(hSSSidebandData) std::cout << "h_ZWindowSS-Sideband_nominal_data found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_data not found" <<std::endl;
  if(hSSSidebandMC) std::cout << "h_ZWindowSS-Sideband_nominal_Zee found" <<std::endl; else std::cout << "h_ZWindowSS-Sideband_nominal_Zee not found" <<std::endl;

  //hOSCenterData->Add(hSSCenterData);
  //hOSSidebandData->Add(hSSSidebandData);

  std::cout << " data charge-flip measurement " << std::endl;
  // NumericalMinimizer NM1(hOSCenterData,hSSCenterData,hOSSidebandData,hSSSidebandData,1e9);
  NumericalMinimizer NM1(hOSCenterData,hSSCenterData,hOSSidebandData,hSSSidebandData,1.1*1e6);
  std::cout << " MC charge-flip measurement " << std::endl;
  // NumericalMinimizer NM2(hOSCenterMC,hSSCenterMC,hOSSidebandMC,hSSSidebandMC,5e9);
  NumericalMinimizer NM2(hOSCenterMC,hSSCenterMC,0,0,1.1*1e6);

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
  leg->AddEntry(NM2.m_flipRateEta,"#font[42]{Sherpa 2.2.1 Z#rightarrow ee}","lpe0");

  TCanvas* c1 = new TCanvas("c1","c1",600,600);
  c1->cd();
  std::vector<TH1D*> c1h1vec;
  c1h1vec.push_back(NM2.m_flipRateEta);
  drawComparison2(c1,&c1h1vec,NM1.m_flipRateEta,"f(#eta)","|#eta|",1e-2,20,0,2.5);
  gROOT->ProcessLine("pad_1->SetLogy();");
  ATLASLabel(0.20,0.83,"Preliminary",1);
  myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  myText(0.60,0.75,1,"P(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
  leg->Draw();
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
  std::vector<TH1D*> c2h1vec;
  c2h1vec.push_back(NM2.m_flipRatePt);
  drawComparison2(c2,&c2h1vec,NM1.m_flipRatePt,"#sigma(p_{T})","p_{T} [GeV]",0,0.2,30,400,true);
  ATLASLabel(0.20,0.83,"Preliminary",1);
  myText(0.20,0.75,1,"#sqrt{s} = 13 TeV, 36.1 fb^{-1}");
  myText(0.60,0.75,1,"P(p_{T},#eta) = #sigma(p_{T}) #times f(#eta)");
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



  TH1D* etaRatio = (TH1D*) NM1.m_flipRateEta->Clone();
  TH1D* ptRatio = (TH1D*) NM1.m_flipRatePt->Clone();

  etaRatio->Divide(NM2.m_flipRateEta);
  ptRatio->Divide(NM2.m_flipRatePt);

  //TF1 * ptFit = new TF1("ptFit","[0]*TMath::Log(log(x-[1]))",30,5000);
  //ptRatio->Fit("ptFit","goff","",30,1000);

  //gROOT->ProcessLine("pad_2->cd();");
  //ptFit->Draw("same");

  TFile *outfile = new TFile("chargeFlipRate.root","RECREATE");
  NM1.m_flipRateEta->SetName("dataEtaRate");
  NM1.m_flipRateEta->Write();
  NM1.m_flipRatePt->SetName("dataPtRate");
  NM1.m_flipRatePt->Write();
  NM2.m_flipRateEta->SetName("MCEtaRate");
  NM2.m_flipRateEta->Write();
  NM2.m_flipRatePt->SetName("MCPtRate");
  NM2.m_flipRatePt->Write();
  etaRatio->SetName("etaFunc");
  etaRatio->Write();
  ptRatio->SetName("ptFunc");
  ptRatio->Write();
  //ptFit->Write();

  ROOT::Math::Minimizer* m_min1 = NM1.m_min;
  ROOT::Math::Minimizer* m_min2 = NM2.m_min;
  int nbinxcorr = NM1.m_flipRateEta->GetNbinsX()+NM1.m_flipRatePt->GetNbinsX();
  TH2F* corrMatrix1 = new TH2F("corrM1","corrM1",nbinxcorr,0,nbinxcorr,nbinxcorr,0,nbinxcorr);
  TH2F* corrMatrix2 = new TH2F("corrM2","corrM2",nbinxcorr,0,nbinxcorr,nbinxcorr,0,nbinxcorr);
  for (unsigned int i = 1; i <= nbinxcorr; i++){
    for (unsigned int j = 1; j <= nbinxcorr; j++){
      corrMatrix1->SetBinContent(i,j, m_min1->Correlation(i-1,j-1) );
      corrMatrix2->SetBinContent(i,j, m_min2->Correlation(i-1,j-1) );
    }
  }
  for (unsigned int i = 1; i <= NM1.m_flipRateEta->GetNbinsX(); i++){
    corrMatrix1->GetXaxis()->SetBinLabel(i,Form("eta%d",i));
    corrMatrix1->GetYaxis()->SetBinLabel(i,Form("eta%d",i));
    corrMatrix2->GetXaxis()->SetBinLabel(i,Form("eta%d",i));
    corrMatrix2->GetYaxis()->SetBinLabel(i,Form("eta%d",i));
  }
  for (unsigned int i = NM1.m_flipRateEta->GetNbinsX()+1; i <= nbinxcorr; i++){
    corrMatrix1->GetXaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
    corrMatrix1->GetYaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
    corrMatrix2->GetXaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
    corrMatrix2->GetYaxis()->SetBinLabel(i,Form("pt%d",i-NM1.m_flipRateEta->GetNbinsX()));
  }
  corrMatrix1->Scale(100.);
  corrMatrix1->GetXaxis()->LabelsOption("v");
  corrMatrix2->Scale(100.);
  corrMatrix2->GetXaxis()->LabelsOption("v");

  gStyle->SetPaintTextFormat("3.0f");


  TCanvas c3("c3","c3",800,600);
  c3.SetRightMargin(0.2);
  c3.SetLeftMargin(0.12);
  corrMatrix1->Draw("colz text");
  corrMatrix1->GetYaxis()->SetTitle("parameter");
  corrMatrix1->GetYaxis()->SetTitleOffset(1.0);
  corrMatrix1->GetXaxis()->SetTitle("parameter");
  corrMatrix1->GetXaxis()->SetNoExponent();
  corrMatrix1->GetXaxis()->SetMoreLogLabels();
  corrMatrix1->GetZaxis()->SetTitle("Correlation [%]");
  corrMatrix1->GetZaxis()->SetTitleOffset(1.5);
  ATLASLabel(0.18,0.90,"internal",0);
  myText(0.18,0.85,0,"data flip-rate fit");


  TCanvas c4("c4","c4",800,600);
  c4.SetRightMargin(0.2);
  c4.SetLeftMargin(0.12);
  corrMatrix2->Draw("colz text");
  corrMatrix2->GetYaxis()->SetTitle("parameter");
  corrMatrix2->GetYaxis()->SetTitleOffset(1.0);
  corrMatrix2->GetXaxis()->SetTitle("parameter");
  corrMatrix2->GetXaxis()->SetNoExponent();
  corrMatrix2->GetXaxis()->SetMoreLogLabels();
  corrMatrix2->GetZaxis()->SetTitle("Correlation [%]");
  corrMatrix2->GetZaxis()->SetTitleOffset(1.5);
  ATLASLabel(0.18,0.90,"internal",0);
  myText(0.18,0.85,0,"MC flip-rate fit");


  c1->Print("chargeFlipEta.eps");
  c2->Print("chargeFlipPt.eps");

  c3.Print("chargeFlipCorrMatrixData.eps");
  c4.Print("chargeFlipCorrMatrixMC.eps");

  outfile->Close();

}