{
  // Load ATLAS style
  gROOT->LoadMacro("/ceph/grid/home/atlas/miham/AnalysisCode/ssdilep/scripts/atlasstyle-00-03-05/AtlasStyle.C");
  gROOT->LoadMacro("/ceph/grid/home/atlas/miham/AnalysisCode/ssdilep/scripts/atlasstyle-00-03-05/AtlasLabels.C");
  gROOT->LoadMacro("/ceph/grid/home/atlas/miham/AnalysisCode/ssdilep/scripts/atlasstyle-00-03-05/AtlasUtils.C");
  SetAtlasStyle();
}

TH1D* drawComparison2(TCanvas* can, TH1D* h1, TH1D* h2, const char* Ytitle, const char* Xtitle, double ydown = 0, double yup = 0, double xmin = 0, double xmax = 0, bool logx = false, 
	double ratioDown = 0.5, double ratioUp = 1.5, bool ratioOrSub = true, TF1* ratioFun = 0)
{    
    can->cd();
    //h1->GetXaxis()->SetRangeUser(xmin,xmax);
    //h2->GetXaxis()->SetRangeUser(xmin,xmax);

    //bool logx = true;

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


	if (logx) {
		pad_1->SetLogx();
		h2->GetXaxis()->SetNoExponent();
		h2->GetXaxis()->SetMoreLogLabels();
		h2->GetXaxis()->SetNdivisions(1040);
	}
    gPad->RedrawAxis("g");

	pad_2->cd();
	TH1D* ratio = (TH1D*) h2->Clone();
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
			ratio->SetBinContent(i, y1/y2 );
			ratio->SetBinError(i, sqrt( ey1*ey1 + ey2*ey2 ) );
		}
		else {
			ratio->SetBinContent(i, y1-y2 );
			ratio->SetBinError(i, sqrt( ey1*ey1 + ey2*ey2 ) );
		}
	}
	ratio->Draw("AxisPE0X0");
	ratio->GetXaxis()->SetLabelSize(0.15);
	ratio->GetYaxis()->SetLabelSize(0.13);
	ratio->GetYaxis()->SetDecimals();
	ratio->GetXaxis()->SetTitle(Xtitle);
	ratio->GetXaxis()->SetTitleSize(0.15);
	ratio->GetXaxis()->SetTitleOffset(1.0);
	if(ratioOrSub) ratio->GetYaxis()->SetTitle("Ratio");
	else           ratio->GetYaxis()->SetTitle("Difference");
	//ratio->GetYaxis()->CenterTitle();
	ratio->GetYaxis()->SetTitleSize(0.15);
	ratio->GetYaxis()->SetTitleOffset(0.40);
	ratio->GetYaxis()->SetRangeUser(ratioDown,ratioUp);
	ratio->GetYaxis()->SetNdivisions(106);
	ratio->SetMarkerSize(0.8);

    TLine *line = new TLine(xmin,(ratioOrSub?1:0),xmax,(ratioOrSub?1:0));
    line->SetLineColor(kRed);
	gPad->RedrawAxis("g");
    line->Draw();
	ratio->Draw("sameE0X0");

    if(ratioFun){
      ratioFun->Draw("same");
	}

	if (logx) {
		pad_2->SetLogx();
		ratio->GetXaxis()->SetNoExponent();
		ratio->GetXaxis()->SetMoreLogLabels();
		ratio->GetXaxis()->SetNdivisions(1040);
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
