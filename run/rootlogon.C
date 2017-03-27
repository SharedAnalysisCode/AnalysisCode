{
  // Load ATLAS style
  gROOT->LoadMacro("/ceph/grid/home/atlas/miham/AnalysisCode/ssdilep/scripts/atlasstyle-00-03-05/AtlasStyle.C");
  gROOT->LoadMacro("/ceph/grid/home/atlas/miham/AnalysisCode/ssdilep/scripts/atlasstyle-00-03-05/AtlasLabels.C");
  gROOT->LoadMacro("/ceph/grid/home/atlas/miham/AnalysisCode/ssdilep/scripts/atlasstyle-00-03-05/AtlasUtils.C");
  SetAtlasStyle();
}

TGraphAsymmErrors* myMakeBand_2(TGraphErrors* g0, TGraphErrors* g1,TGraphErrors* g2) {
  // default is g0
    //const Int_t debug=0;

  TGraphAsymmErrors* g3= new TGraphAsymmErrors();

  Double_t  x1=0., y1=0., x2=0., y2=0., y0=0, x3=0.;
  //Double_t dx1=0.;
  Double_t dum;
  for (Int_t i=0; i<g1->GetN(); i++) {
    g0->GetPoint(i, x1,y0);
    g1->GetPoint(i, x1,y1);
    g2->GetPoint(i, x1,y2);

    // if (y1==0) y1=1;
    //if (y2==0) y2=1;

    if (i==g1->GetN()-1) x2=x1;
    else                 g2->GetPoint(i+1,x2,dum);

    if (i==0)            x3=x1;
    else                 g2->GetPoint(i-1,x3,dum);

    Double_t tmp=y2;
    if (y1<y2) {y2=y1; y1=tmp;}
    //Double_t y3=1.;
    Double_t y3=y0;
    g3->SetPoint(i,x1,y3);

    Double_t binwl=(x1-x3)/2.;
    Double_t binwh=(x2-x1)/2.;
    if (binwl==0.)  binwl= binwh;
    if (binwh==0.)  binwh= binwl;
    g3->SetPointError(i,g0->GetEX()[i],g0->GetEX()[i],(y3-y2),(y1-y3));

  }
  return g3;

}

TGraphAsymmErrors* myTGraphErrorsDivide_2(TGraphAsymmErrors* g1,TGraphErrors* g2) {

  const Int_t debug=0; 

  TGraphAsymmErrors* g3= new TGraphAsymmErrors();
  Int_t n1=g1->GetN();
  Int_t n2=g2->GetN();

  if (n1!=n2) {
    printf(" vectors do not have same number of entries !  \n");
   return g3;
  }

  Double_t   x1=0.,   y1=0., x2=0., y2=0.;
  Double_t dx1h=0., dx1l=0.;
  Double_t dy1h=0., dy1l=0.;
  Double_t dy2h=0., dy2l=0.;

  Double_t* X1 = g1->GetX();
  Double_t* Y1 = g1->GetY();
  Double_t* EXhigh1 = g1->GetEXhigh();
  Double_t* EXlow1 =  g1->GetEXlow();
  Double_t* EYhigh1 = g1->GetEYhigh();
  Double_t* EYlow1 =  g1->GetEYlow();

  Double_t* X2 = g2->GetX();
  Double_t* Y2 = g2->GetY();
  Double_t* EXhigh2 = g2->GetEX();
  Double_t* EXlow2 =  g2->GetEX();
  Double_t* EYhigh2 = g2->GetEY();
  Double_t* EYlow2 =  g2->GetEY();

  for (Int_t i=0; i<g1->GetN(); i++) {
    g1->GetPoint(i,x1,y1);
    g2->GetPoint(i,x2,y2);
    dx1h  = EXhigh1[i];
    dx1l  = EXlow1[i];
    if (y1!=0.) dy1h  = EYhigh1[i]/y1;
    else        dy1h  = 0.;
    if (y2!=0.) dy2h  = EYhigh2[i]/y2;
    else        dy2h  = 0.;
    if (y1!=0.) dy1l  = EYlow1 [i]/y1;
    else        dy1l  = 0.;
    if (y2!=0.) dy2l  = EYlow2 [i]/y2;
    else        dy2l  = 0.;
   
    //if (debug)
    //printf("%d x1=%f x2=%f y1=%f y2=%f  \n",i,x1,x2,y1,y2);
    if (debug)
      printf("%d dy1=%f %f dy2=%f %f sqrt= %f %f \n",i,dy1l,dy1h,dy2l,dy2h,
	     std::sqrt(dy1l*dy1l+dy2l*dy2l), std::sqrt(dy1h*dy1h+dy2h*dy2h));

    if (y2!=0.) g3->SetPoint(i, x1,y1/y2);
    else       g3->SetPoint(i, x1,y2);
    Double_t el=0.; Double_t eh=0.;

    if (y1!=0. && y2!=0.) el=std::sqrt(dy1l*dy1l/*+dy2l*dy2l*/)*(y1/y2);
    if (y1!=0. && y2!=0.) eh=std::sqrt(dy1h*dy1h/*+dy2h*dy2h*/)*(y1/y2);

    if (debug) printf("dx1h=%f  dx1l=%f  el=%f  eh=%f \n",dx1h,dx1l,el,eh);
    g3->SetPointError(i,dx1h,dx1l,el,eh);

  }  
  return g3;

}

TGraphErrors* TH1TOTGraph_2(TH1 *h1, double n=1, double nAll=1, bool errorX = true){


  if (!h1) std::cout << "TH1TOTGraph: histogram not found !" << std::endl;

 TGraphErrors* g1= new TGraphErrors();

 Double_t x, y, ex, ey, w, w3;
 for (Int_t i=1; i<=h1->GetNbinsX(); i++) {
   w=h1->GetXaxis()->GetBinWidth(i);
  w3=(w/2.)*2/4;


   y=h1->GetBinContent(i);
  ey=h1->GetBinError(i);
   x= nAll!=1 ? h1->GetBinCenter(i)-w3+2*((n-1)/(nAll-1))*w3 : h1->GetBinCenter(i);
  if (errorX)
  	ex=h1->GetBinWidth(i)/2;
  else
  	ex=0;

  // std::cout << "w: " << w << " w3: " << w3 << " n: " << n << " nAll: " << nAll << " h1->GetBinCenter(i): " << h1->GetBinCenter(i) << " x: " << x << std::endl;
 
   g1->SetPoint(i-1,x,y);
   g1->SetPointError(i-1,ex,ey);

 }

 //g1->Print();

 return g1;
}

TH1D* drawComparison2(TCanvas* can, std::vector<TH1D* > *h1vec, TH1D* h2, const char* Ytitle, const char* Xtitle, double ydown = 0, double yup = 0, double xmin = 0, double xmax = 0, bool logx = false, 
	double ratioDown = 0.5, double ratioUp = 1.5, bool ratioOrSub = true, TF1* ratioFun = 0, bool invertColor = false, std::string drawOpt = "PE0", bool verticalLines = false, TGraphAsymmErrors* sysBand = 0)
{    
    can->cd();
    //h1->GetXaxis()->SetRangeUser(xmin,xmax);
    //h2->GetXaxis()->SetRangeUser(xmin,xmax);

    //bool logx = true;

    TH1D* h1 = h1vec->at(0);

	TPad* pad_1=NULL;
	TPad* pad_2=NULL;
	pad_1 = new TPad("pad_1", "up", 0., 0.299, 1., 1.);
	pad_1->SetBottomMargin(0.03);
	pad_1->SetTopMargin(0.08);
	pad_1->Draw();

	pad_2= new TPad("pad_2", "down", 0.0, 0.0, 1.0, 0.301);
	pad_2->SetTopMargin(0.03);
	pad_2->SetBottomMargin(0.35);
	//pad_2->SetGridx();
	pad_2->SetGridy();
	pad_2->Draw();

	pad_1->cd();
	h1->Draw("PE0");
	h1->SetMarkerSize(0.8);
	//h1->Draw("histoH");
	if( !(ydown == 0  && yup == 0) ){
		h1->SetMaximum(yup);
		h1->SetMinimum(ydown);
	}
	h1->GetXaxis()->SetLabelSize(0);
	h1->GetYaxis()->SetLabelSize(0.06);
	h1->GetYaxis()->SetNdivisions(515);
	h1->GetYaxis()->SetTitle(Ytitle);
	h1->GetYaxis()->SetTitleSize(0.07);
	h1->GetYaxis()->SetTitleOffset(0.95);

	h2->Draw("PE0same");
	h2->SetMarkerSize(0.8);

	for (unsigned int i = 1; i < h1vec->size(); i++){
		h1vec->at(i)->SetMarkerSize(0.8);
		h1vec->at(i)->Draw("PE0same");
	}


	if (logx) {
		pad_1->SetLogx();
		h2->GetXaxis()->SetNoExponent();
		h2->GetXaxis()->SetMoreLogLabels();
		h2->GetXaxis()->SetNdivisions(1040);
	}
    gPad->RedrawAxis("g");

	pad_2->cd();
	TH1D* ratio = (TH1D*) h2->Clone();
	TGraphErrors* ratioGr = nullptr;
	for (int i = 1; i < h1->GetNbinsX()+1; i++){
		double y1 = ratio->GetBinContent(i);
		double y2 = h1->GetBinContent(i);
		double ey1 = ratio->GetBinError(i) / (ratioOrSub?y1:1);
		double ey2 = h1->GetBinError(i) / (ratioOrSub?y2:1);
		if (!y2 || !y1) {
			ratio->SetBinContent(i, -100 );
			ratio->SetBinError(i, 0 );	
		}
		else if (ratioOrSub) {
			ratio->SetBinContent(i, !invertColor ? y1/y2 : y2/y1 );
			ratio->SetBinError(i, sqrt( ey1*ey1 + ey2*ey2 ) );
		}
		else {
			ratio->SetBinContent(i, !invertColor ? y1-y2 : y2-y1 );
			ratio->SetBinError(i, sqrt( ey1*ey1 + ey2*ey2 ) );
		}
	}
	if (invertColor) {
		ratio->SetMarkerColor(h1->GetMarkerColor());
		ratio->SetLineColor(h1->GetLineColor());
	}
	ratioGr = TH1TOTGraph_2(ratio,1,h1vec->size(),false);
	ratioGr->SetMarkerSize(0.8);
	ratioGr->SetMarkerColor(ratio->GetMarkerColor());
	ratioGr->SetLineColor(ratio->GetLineColor());
	std::vector<TH1D*> ratioVec;
	std::vector<TGraphErrors*> ratioVecGr;
	for (unsigned int ivec = 1; ivec < h1vec->size(); ivec++){
		TH1D* ratio = (TH1D*) h2->Clone();
		for (int i = 1; i < h1->GetNbinsX()+1; i++){
			double y1 = ratio->GetBinContent(i);
			double y2 = h1vec->at(ivec)->GetBinContent(i);
			double ey1 = ratio->GetBinError(i) / (ratioOrSub?y1:1);
			double ey2 = h1vec->at(ivec)->GetBinError(i) / (ratioOrSub?y2:1);
			if (!y2 || !y1) {
				ratio->SetBinContent(i, -100 );
				ratio->SetBinError(i, 0 );

			}
			else if (ratioOrSub) {
				ratio->SetBinContent(i, !invertColor ? y1/y2 : y2/y1 );
				ratio->SetBinError(i, sqrt( ey1*ey1 + ey2*ey2 ) );
			}
			else {
				ratio->SetBinContent(i, !invertColor ? y1-y2 : y2-y1 );
				ratio->SetBinError(i, sqrt( ey1*ey1 + ey2*ey2 ) );
			}
		}
		if (invertColor) {
			ratio->SetMarkerColor(h1vec->at(ivec)->GetMarkerColor());
			ratio->SetLineColor(h1vec->at(ivec)->GetLineColor());
		}
		ratioVec.push_back(ratio);
		TGraphErrors* ratioGr_temp = TH1TOTGraph_2(ratio,ivec+1,h1vec->size(),false);
		ratioGr_temp->SetMarkerSize(0.8);
		ratioGr_temp->SetMarkerColor(ratio->GetMarkerColor());
		ratioGr_temp->SetLineColor(ratio->GetLineColor());
		ratioVecGr.push_back(ratioGr_temp);
    }
	ratioGr->Draw(Form("A %s",drawOpt.c_str()));
	ratioGr->GetXaxis()->SetLabelSize(0.15);
	ratioGr->GetYaxis()->SetLabelSize(0.13);
	ratioGr->GetYaxis()->SetDecimals();
	ratioGr->GetXaxis()->SetTitle(Xtitle);
	ratioGr->GetXaxis()->SetTitleSize(0.15);
	ratioGr->GetXaxis()->SetTitleOffset(1.0);
	if(ratioOrSub) ratioGr->GetYaxis()->SetTitle("Ratio");
	else           ratioGr->GetYaxis()->SetTitle("Difference");
	//ratio->GetYaxis()->CenterTitle();
	ratioGr->GetYaxis()->SetTitleSize(0.15);
	ratioGr->GetYaxis()->SetTitleOffset(0.40);
	ratioGr->GetYaxis()->SetRangeUser(ratioDown,ratioUp);
	ratioGr->GetXaxis()->SetLimits(xmin,xmax);
	ratioGr->GetYaxis()->SetNdivisions(106);
	ratioGr->SetMarkerSize(0.8);

	if (verticalLines) {
		for (int i = 1; i <= h1->GetNbinsX(); i++ ){
			TLine *line = new TLine(h1->GetXaxis()->GetBinLowEdge(i),ratioDown,h1->GetXaxis()->GetBinLowEdge(i),ratioUp);
			line->SetLineColor(kBlack);
			line->SetLineStyle(3);
			line->Draw();
		}
	}
    if(sysBand){
	  TGraphAsymmErrors* relativeSysBand;
	  TH1D* tempHisto = (TH1D*) h1->Clone();
	  TGraphErrors* MC = TH1TOTGraph_2( tempHisto );
	  relativeSysBand = myTGraphErrorsDivide_2(sysBand,MC);
	  relativeSysBand->Draw("sameE2");
	  relativeSysBand->SetFillColor(kYellow);
	  // relativeSysBand->SetFillStyle(3244);
	  ratioGr->Draw(Form("same %s",drawOpt.c_str()));
	}
	TLine *line = new TLine(xmin,(ratioOrSub?1:0),xmax,(ratioOrSub?1:0));
	line->SetLineColor(kRed);
	gPad->RedrawAxis("g");
	line->Draw();
	ratioGr->Draw(Form("same %s",drawOpt.c_str()));
	for (unsigned int i = 0; i<ratioVecGr.size(); i++){
		ratioVecGr.at(i)->GetXaxis()->SetLimits(xmin,xmax);
		ratioVecGr.at(i)->Draw(Form("same %s",drawOpt.c_str()));
	}
	if(ratioFun){
		ratioFun->Draw("same");
	}

	if (logx) {
		pad_2->SetLogx();
		ratioGr->GetXaxis()->SetNoExponent();
		ratioGr->GetXaxis()->SetMoreLogLabels();
		ratioGr->GetXaxis()->SetNdivisions(1040);
	}

	pad_1->cd();

	return ratio;
}

void histo_overUnderFlow(TH1* his) {
	int NbinsX = his->GetNbinsX();
    //his->SetBinContent(NbinsX,his->GetBinContent(NbinsX)+his->GetBinContent(NbinsX+1));
    //his->SetBinError(NbinsX, 
    //	sqrt( pow(his->GetBinError(NbinsX),2) + pow(his->GetBinError(NbinsX+1),2) ) );
    his->SetBinContent(NbinsX+1,0);
    his->SetBinError(NbinsX+1,0);
    his->SetBinContent(0,0);
    his->SetBinError(0,0); 

    return;
}

