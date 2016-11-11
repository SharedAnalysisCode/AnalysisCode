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

	double m_ptBins[11] = {30., 40., 50., 60., 70., 80., 90., 100., 125., 150., 200.};
    double m_etaBins[10] = {0.0, 0.75, 1.1, 1.37, 1.52, 1.7, 1.9, 2.1, 2.3, 2.5};

	int m_NetaBins;
	int m_NptBins;

	ROOT::Math::Minimizer* NumericalMinimization1D(const char*, const char*, int);
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
}

//-------------------------------------------------
// ROOT::Math::Minimizer --------------------------
//-------------------------------------------------
ROOT::Math::Minimizer* NumericalMinimizer::NumericalMinimization1D(const char * minName = "Minuit2",
                          const char *algoName = "" ,
                          int randomSeed = -1)
{
   ROOT::Math::Minimizer* min =
      ROOT::Math::Factory::CreateMinimizer(minName, algoName);

   // set tolerance , etc...
   min->SetMaxFunctionCalls(1e7); // for Minuit/Minuit2
   min->SetMaxIterations(1e5);  // for GSL
   min->SetTolerance(1e-5);
   min->SetPrintLevel(1);

   // create funciton wrapper for minmizer
   // a IMultiGenFunction type
   auto func = &NumericalMinimizer::LogLikelihood1D;
   ROOT::Math::Functor f( &(this->*func) ,m_NetaBins+m_NptBins);

   min->SetFunction(f);

   // Set the free variables to be minimized!
   int index = 0;
   double stepSize = 1e-5;
   for (int eta = 1; eta <= m_NetaBins; eta++){
    std::ostringstream name;
    name << "eta" << eta;
    min->SetVariable(index,name.str().c_str(),0,stepSize);
    min->SetVariableLowerLimit(index,stepSize);
    //min->SetVariableUpperLimit(index,1.0);
    index++;
   }
   for (int pt = 1; pt <= m_NptBins; pt++){
    std::ostringstream name;
    name << "pt" << pt;
    min->SetVariable(index,name.str().c_str(),0,stepSize);
    min->SetVariableLowerLimit(index,stepSize);
    //min->SetVariableUpperLimit(index,1.0);
    index++;
   }


   // do the minimization
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
					int totBin = ( (pt1-1)*m_NetaBins + eta1-1 )*m_NptBins*m_NetaBins + ( (pt2-1)*m_NetaBins + eta2 );
					value += -m_hSSCenter->GetBinContent(totBin) * log (xx[eta1-1]*xx[m_NetaBins+pt1-1] + xx[eta2-1]*xx[m_NetaBins+pt2-1] ) 
					+ m_hOSCenter->GetBinContent(totBin)*( xx[eta1-1]*xx[m_NetaBins+pt1-1] + xx[eta2-1]*xx[m_NetaBins+pt2-1]  );
				}
			}
		}
	}
	double etaNorm = 0;
	for(int eta1 = 0; eta1 < m_NetaBins; eta1++) {
		if(eta1==4) continue;
		etaNorm += (m_etaBins[eta1+1]-m_etaBins[eta1])*xx[eta1];
	}
	return value + 1e8*pow((etaNorm-1),2);
}

void charge_flip_measurement(){

	std::string OSCenterInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowOS_Powheg.root";
	std::string OSSidebandInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowOS-Sideband_Powheg.root";
	std::string SSCenterInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowSS_Powheg.root";
	std::string SSSidebandInputFile = "/ceph/grid/home/atlas/miham/AnalysisCode/run/Plots/hists_chargeFlipHist_ZWindowSS-Sideband_Powheg.root";

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

	NumericalMinimizer NM1(hOSCenterData,hSSCenterData,hOSSidebandData,hSSSidebandData);

}