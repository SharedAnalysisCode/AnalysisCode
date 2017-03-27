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



// Double_t langaufun(Double_t *x, Double_t *par) {

//    //Fit parameters:
//    //par[0]=Width (scale) parameter of Landau density
//    //par[1]=Most Probable (MP, location) parameter of Landau density
//    //par[2]=Total area (integral -inf to inf, normalization constant)
//    //par[3]=Width (sigma) of convoluted Gaussian function
//    //
//    //In the Landau distribution (represented by the CERNLIB approximation),
//    //the maximum is located at x=-0.22278298 with the location parameter=0.
//    //This shift is corrected within this function, so that the actual
//    //maximum is identical to the MP parameter.

//       // Numeric constants
//       Double_t invsq2pi = 0.3989422804014;   // (2 pi)^(-1/2)
//       Double_t mpshift  = -0.22278298;       // Landau maximum location

//       // Control constants
//       Double_t np = 100.0;      // number of convolution steps
//       Double_t sc =   5.0;      // convolution extends to +-sc Gaussian sigmas

//       // Variables
//       Double_t xx;
//       Double_t mpc;
//       Double_t fland;
//       Double_t sum = 0.0;
//       Double_t xlow,xupp;
//       Double_t step;
//       Double_t i;


//       // MP shift correction
//       mpc = par[1] - mpshift * par[0];

//       // Range of convolution integral
//       xlow = x[0] - sc * par[3];
//       xupp = x[0] + sc * par[3];

//       step = (xupp-xlow) / np;

//       // Convolution integral of Landau and Gaussian by sum
//       for(i=1.0; i<=np/2; i++) {
//          xx = xlow + (i-.5) * step;
//          fland = TMath::Landau(xx,mpc,par[0]) / par[0];
//          sum += fland * TMath::Gaus(x[0],xx,par[3]);

//          xx = xupp - (i-.5) * step;
//          fland = TMath::Landau(xx,mpc,par[0]) / par[0];
//          sum += fland * TMath::Gaus(x[0],xx,par[3]);
//       }

//       return (par[2] * step * sum * invsq2pi / par[3]);
// }



// TF1 *langaufit(TH1F *his, Double_t *fitrange, Double_t *startvalues, Double_t *parlimitslo, Double_t *parlimitshi, Double_t *fitparams, Double_t *fiterrors, Double_t *ChiSqr, Int_t *NDF)
// {
//    // Once again, here are the Landau * Gaussian parameters:
//    //   par[0]=Width (scale) parameter of Landau density
//    //   par[1]=Most Probable (MP, location) parameter of Landau density
//    //   par[2]=Total area (integral -inf to inf, normalization constant)
//    //   par[3]=Width (sigma) of convoluted Gaussian function
//    //
//    // Variables for langaufit call:
//    //   his             histogram to fit
//    //   fitrange[2]     lo and hi boundaries of fit range
//    //   startvalues[4]  reasonable start values for the fit
//    //   parlimitslo[4]  lower parameter limits
//    //   parlimitshi[4]  upper parameter limits
//    //   fitparams[4]    returns the final fit parameters
//    //   fiterrors[4]    returns the final fit errors
//    //   ChiSqr          returns the chi square
//    //   NDF             returns ndf

//    Int_t i;
//    Char_t FunName[100];

//    sprintf(FunName,"Fitfcn_%s",his->GetName());

//    TF1 *ffitold = (TF1*)gROOT->GetListOfFunctions()->FindObject(FunName);
//    if (ffitold) delete ffitold;

//    TF1 *ffit = new TF1(FunName,langaufun,fitrange[0],fitrange[1],4);
//    ffit->SetParameters(startvalues);
//    ffit->SetParNames("Width","MP","Area","GSigma");

//    for (i=0; i<4; i++) {
//       ffit->SetParLimits(i, parlimitslo[i], parlimitshi[i]);
//    }

//    his->Fit(FunName,"RB0");   // fit within specified range, use ParLimits, do not plot

//    ffit->GetParameters(fitparams);    // obtain fit parameters
//    for (i=0; i<4; i++) {
//       fiterrors[i] = ffit->GetParError(i);     // obtain fit parameter errors
//    }
//    ChiSqr[0] = ffit->GetChisquare();  // obtain chi^2
//    NDF[0] = ffit->GetNDF();           // obtain ndf

//    return (ffit);              // return fit function

// }


// using namespace RooFit;

//   TFile f("myZPeakCRAB.root");
//   Z_mass=(TH1F*)Zmass->Clone();
//  double hmin = Z_mass->GetXaxis()->GetXmin();
//  double hmax = Z_mass->GetXaxis()->GetXmax();

//   // Declare observable x
//   RooRealVar x("x","x",hmin,hmax) ;
//   RooDataHist dh("dh","dh",x,Import(*Z_mass)) ;

//   RooPlot* frame = x.frame(Title("Z mass")) ;
//   dh.plotOn(frame,MarkerColor(2),MarkerSize(0.9),MarkerStyle(21));  //this will show histogram data points on canvas 
//   dh.statOn(frame);  //this will display hist stat on canvas

//   RooRealVar mean("mean","mean",95.0, 70.0, 120.0);
//   RooRealVar width("width","width",5.0, 0.0, 120.0);
//   RooRealVar sigma("sigma","sigma",5.0, 0.0, 120.0);
// //  RooGaussian gauss("gauss","gauss",x,mean,sigma);
//   RooBreitWigner gauss("gauss","gauss",x,mean,sigma);
//  // RooVoigtian gauss("gauss","gauss",x,mean,width,sigma);

//   RooFitResult* filters = gauss.fitTo(dh,"qr");
//   gauss.plotOn(frame,LineColor(4));//this will show fit overlay on canvas 
//   gauss.paramOn(frame); //this will display the fit parameters on canvas
//   //filters->Print("v");

//   // Draw all frames on a canvas
//   TCanvas* c = new TCanvas("ZmassHisto","ZmassHisto",800,400) ;
//   c->cd() ; gPad->SetLeftMargin(0.15);
           
//             frame->GetXaxis()->SetTitle("Z mass (in GeV/c^{2})");  frame->GetXaxis()->SetTitleOffset(1.2);
//       float binsize = Z_mass->GetBinWidth(1); char Bsize[50]; 
//             //sprintf(Bsize,"Events per %2.2f",binsize);
//             // frame->GetYaxis()->SetTitle(Bsize);  
//              //frame->GetYaxis()->SetTitleOffset(1.2);
//             frame->Draw() ;
//             c->Print("myZmaa.eps");  

// }


{

  using namespace RooFit;

  TFile* ZeeAS   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_invMassPeak_ZWindowAS_CF.root");
  // TFile* ZeeSS   = new TFile("/afs/f9.ijs.si/home/miham/AnalysisCode/run/CFclosure/hists_invMassPeak_ZWindowSS_CF.root");

  TH1D* hZeeAS = (TH1D*) ZeeAS->Get("h_ZWindowAS_nominal_data");
  // TH1D* hZeeSS = (TH1D*) ZeeSS->Get("h_ZWindowSS_nominal_data");

  double hmin = 80;
  double hmax = 100;

  // Declare observable x
  RooRealVar x("x","x",hmin,hmax) ;
  RooDataHist dh("dh","dh",x,Import(*hZeeAS)) ;

  RooPlot* frame = x.frame(Title("Z mass")) ;
  dh.plotOn(frame,MarkerColor(2),MarkerSize(0.9),MarkerStyle(21));  //this will show histogram data points on canvas 
  dh.statOn(frame);  //this will display hist stat on canvas

  RooRealVar mean("mean","mean",95.0, 70.0, 120.0);
  RooRealVar width("width","width",5.0, 0.0, 120.0);
  RooRealVar sigma("sigma","sigma",5.0, 0.0, 120.0);
  //  RooGaussian gauss("gauss","gauss",x,mean,sigma);
  RooBreitWigner gauss("gauss","gauss",x,mean,sigma);
  // RooVoigtian gauss("gauss","gauss",x,mean,width,sigma);

  RooFitResult* filters = gauss.fitTo(dh,"qr");
  gauss.plotOn(frame,LineColor(4));//this will show fit overlay on canvas 
  gauss.paramOn(frame); //this will display the fit parameters on canvas
  //filters->Print("v");

  // Draw all frames on a canvas
  TCanvas* c = new TCanvas("ZmassHisto","ZmassHisto",800,400) ;
  c->cd() ;
  gPad->SetLeftMargin(0.15);
           
  frame->GetXaxis()->SetTitle("Z mass (in GeV/c^{2})");
  frame->GetXaxis()->SetTitleOffset(1.2);
  float binsize = Z_mass->GetBinWidth(1);
  char Bsize[50]; 
  //sprintf(Bsize,"Events per %2.2f",binsize);
  // frame->GetYaxis()->SetTitle(Bsize);  
  //frame->GetYaxis()->SetTitleOffset(1.2);
  frame->Draw() ;
  c->Print("myZmaa.eps"); 

  
}