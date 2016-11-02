"""
samples.py

author: Will Davey <will.davey@cern.ch> 
created: 2012-10-31
"""

import ROOT
from core import Sample, Var, Weights, PlotDetails, Cut, Selector

## Common weights
kQCD = Var('kQCD_fix')
kEW  = Var('kEW_fix')


#-------------------------------------------------------------------------------
# tau-mu channel data
#-------------------------------------------------------------------------------
data = Sample(
        name =  'data',
        tlatex = 'data',
        fill_color = ROOT.kGreen+2,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        ) 


#-------------------------------------------------------------------------------
# signal samples 
#-------------------------------------------------------------------------------
ZP_pd = PlotDetails(weights=Weights([kQCD]))
Zprime250tautau = Sample(
        name =  'Zprime250tautau',
        tlatex = 'Z\'_{SSM}(250)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = ZP_pd,
        xsec = 3.7396E+01,
        ) 

Zprime500tautau = Sample(
        name =  'Zprime500tautau',
        tlatex = 'Z\'_{SSM}(500)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = ZP_pd,
        xsec = 2.8256,
        ) 

Zprime750tautau = Sample(
        name =  'Zprime750tautau',
        tlatex = 'Z\'_{SSM}(750)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = ZP_pd,
        xsec = 5.3747E-01,
        ) 

Zprime1000tautau = Sample(
        name =  'Zprime1000tautau',
        tlatex = 'Z\'_{SSM}(1000)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = ZP_pd,
        xsec = 1.4845E-01,
        ) 

Zprime1250tautau = Sample(
        name =  'Zprime1250tautau',
        tlatex = 'Z\'_{SSM}(1250)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = ZP_pd,
        xsec = 4.9671E-02,
        ) 


signal = [Zprime250tautau,
          Zprime500tautau,
          Zprime750tautau,
          Zprime1000tautau,
          Zprime1250tautau,
          ]


#-----------------------------------------------------------------------------
# DYtautau
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/ZprimeTauTau2012#Sample_List
#       * kfactors: mass dependent
#-----------------------------------------------------------------------------

## Ztautau 
high_mass_filter = Selector('high_mass_filter',[Cut('RESOMASS<180.e3')])
Ztautau_pd = PlotDetails(selector=high_mass_filter)
Ztautau            = Sample( name = 'Ztautau',            xsec = 8.7804E02, plot_details=Ztautau_pd, fill_color = ROOT.kRed )

## high-mass DYtautau
DYtautau_180M250   = Sample( name = 'DYtautau_180M250',   xsec = 1.2485E-00,fill_color=ROOT.kRed-1)
DYtautau_250M400   = Sample( name = 'DYtautau_250M400',   xsec = 4.3608E-01,fill_color=ROOT.kRed-2 )
DYtautau_400M600   = Sample( name = 'DYtautau_400M600',   xsec = 7.1800E-02,fill_color=ROOT.kRed-3 )
DYtautau_600M800   = Sample( name = 'DYtautau_600M800',   xsec = 1.2235E-02,fill_color=ROOT.kRed-4 )
DYtautau_800M1000  = Sample( name = 'DYtautau_800M1000',  xsec = 3.0727E-03,fill_color=ROOT.kRed-5 )
DYtautau_1000M1250 = Sample( name = 'DYtautau_1000M1250', xsec = 1.0719E-03,fill_color=ROOT.kRed-6 )
DYtautau_1250M1500 = Sample( name = 'DYtautau_1250M1500', xsec = 2.9974E-04,fill_color=ROOT.kRed-7 )
DYtautau_1500M1750 = Sample( name = 'DYtautau_1500M1750', xsec = 9.5176E-05,fill_color=ROOT.kRed-8 )
DYtautau_1750M2000 = Sample( name = 'DYtautau_1750M2000', xsec = 3.2609E-05,fill_color=ROOT.kRed-9 )
DYtautau_2000M2250 = Sample( name = 'DYtautau_2000M2250', xsec = 1.1855E-05,fill_color=ROOT.kRed-10)
DYtautau_2250M2500 = Sample( name = 'DYtautau_2250M2500', xsec = 4.4565E-06,fill_color=ROOT.kGray  )
DYtautau_samples = [DYtautau_180M250,DYtautau_250M400,DYtautau_400M600,DYtautau_600M800,
                    DYtautau_800M1000,DYtautau_1000M1250,DYtautau_1250M1500,DYtautau_1500M1750,
                    DYtautau_1750M2000,DYtautau_2000M2250,DYtautau_2250M2500]

## stitched DYtautau
DYtautau_pd = PlotDetails(weights=Weights([kQCD,kEW]))
#DYtautau_pd = None 

DYtautau = Sample(
        name =  'DYtautau',
        tlatex = 'DY#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = DYtautau_pd,
        daughters = [Ztautau]+DYtautau_samples,
        ) 

## reweighted signal 
wDY1000 = Var('ZP1000_WEIGHT')
Zprime1000tautau_pd = PlotDetails(weights=Weights([kQCD,wDY1000]))

Zprime1000tautau_rw = Sample(
        name =  'Zprime1000tautau_rw',
        tlatex = 'Z\'_{SSM}(1000)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = Zprime1000tautau_pd,
        #daughters = DYtautau_samples,
        daughters = [Ztautau]+DYtautau_samples,
        ) 

wDY1250 = Var('ZP1250_WEIGHT_fix')
Zprime1250tautau_pd = PlotDetails(weights=Weights([kQCD,wDY1250]))

Zprime1250tautau_rw = Sample(
        name =  'Zprime1250tautau_rw',
        tlatex = 'Z\'_{SSM}(1250)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = Zprime1250tautau_pd,
        #daughters = DYtautau_samples,
        daughters = [Ztautau]+DYtautau_samples,
        ) 

wDY1250_nosm = Var('ZP1250_NOSM_WEIGHT_fix')
Zprime1250tautau_nosm_pd = PlotDetails(weights=Weights([kQCD,wDY1250_nosm]))

Zprime1250tautau_rw_nosm = Sample(
        name =  'Zprime1250tautau_rw_nosm',
        tlatex = 'Z\'_{SSM}(1250)#rightarrow#tau#tau',
        fill_color = ROOT.kWhite,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        plot_details = Zprime1250tautau_nosm_pd,
        #daughters = DYtautau_samples,
        daughters = [Ztautau]+DYtautau_samples,
        ) 



signal_rw = [
    Zprime1000tautau_rw,
    Zprime1250tautau_rw,
    Zprime1250tautau_rw_nosm,
        ]



#-----------------------------------------------------------------------------
#  Wenu
# Notes:
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#       July 25 Xsecs: AtlasProtected/TopMC12#MC12_Common_W_jets_Background_Sa (07 July 2012)
#               k-factors: https://twiki.cern.ch/twiki/pub/AtlasProtected/HiggsRecommendationsForSummer2012/8TeVCrossSections.pdf (25 July 2012)
#
#-----------------------------------------------------------------------------
WenuNp0 = Sample( name = 'WenuNp0', xsec = 8037.1*1.19*1.0 )
WenuNp1 = Sample( name = 'WenuNp1', xsec = 1579.2*1.19*1.0 )
WenuNp2 = Sample( name = 'WenuNp2', xsec = 477.2*1.19*1.0 )
WenuNp3 = Sample( name = 'WenuNp3', xsec = 133.93*1.19*1.0 )
WenuNp4 = Sample( name = 'WenuNp4', xsec = 35.622*1.19*1.0 )
WenuNp5 = Sample( name = 'WenuNp5', xsec = 10.553*1.19*1.0 )
Wenu = Sample(
        name =  'Wenu',
        tlatex = 'W#rightarrow#mu#nu',
        fill_color = ROOT.kGray,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        daughters = [WenuNp0, WenuNp1, WenuNp2, WenuNp3, WenuNp4, WenuNp5],
        )


#-----------------------------------------------------------------------------
#  Wmunu
# Notes:
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#       July 25 Xsecs: AtlasProtected/TopMC12#MC12_Common_W_jets_Background_Sa (07 July 2012)
#               k-factors: https://twiki.cern.ch/twiki/pub/AtlasProtected/HiggsRecommendationsForSummer2012/8TeVCrossSections.pdf (25 July 2012)
#
#-----------------------------------------------------------------------------
WmunuNp0 = Sample( name = 'WmunuNp0', xsec = 8040*1.19*1.0 )
WmunuNp1 = Sample( name = 'WmunuNp1', xsec = 1580.3*1.19*1.0 )
WmunuNp2 = Sample( name = 'WmunuNp2', xsec = 477.5*1.19*1.0 )
WmunuNp3 = Sample( name = 'WmunuNp3', xsec = 133.94*1.19*1.0 )
WmunuNp4 = Sample( name = 'WmunuNp4', xsec = 35.636*1.19*1.0 )
WmunuNp5 = Sample( name = 'WmunuNp5', xsec = 10.571*1.19*1.0 )
Wmunu = Sample(
        name =  'Wmunu',
        tlatex = 'W#rightarrow#mu#nu',
        fill_color = ROOT.kGray,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        daughters = [WmunuNp0, WmunuNp1, WmunuNp2, WmunuNp3, WmunuNp4, WmunuNp5],
        )



#-----------------------------------------------------------------------------
# Wtaunu
# Notes:
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#       July 25 Xsecs: AtlasProtected/TopMC12#MC12_Common_W_jets_Background_Sa (07 July 2012)
#                      k-factors: https://twiki.cern.ch/twiki/pub/AtlasProtected/HiggsRecommendationsForSummer2012/8TeVCrossSections.pdf (25 July 2012)
#
#-----------------------------------------------------------------------------
WtaunuNp0 = Sample( name = 'WtaunuNp0', xsec = 8035.8*1.19*1.0 )
WtaunuNp1 = Sample( name = 'WtaunuNp1', xsec = 1579.8*1.19*1.0 )
WtaunuNp2 = Sample( name = 'WtaunuNp2', xsec = 477.55*1.19*1.0 )
WtaunuNp3 = Sample( name = 'WtaunuNp3', xsec = 133.79*1.19*1.0 )
WtaunuNp4 = Sample( name = 'WtaunuNp4', xsec = 35.583*1.19*1.0 )
WtaunuNp5 = Sample( name = 'WtaunuNp5', xsec = 10.54*1.19*1.0 )
Wtaunu = Sample(
        name =  'Wtaunu',
        tlatex = 'W#rightarrow#tau#nu',
        fill_color = ROOT.kRed+1,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        daughters = [WtaunuNp0, WtaunuNp1, WtaunuNp2, WtaunuNp3, WtaunuNp4, WtaunuNp5],
        )



#-----------------------------------------------------------------------------
# Zee
# Notes:
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#       July 25 Xsecs: AtlasProtected/TopMC12#MC12_Common_Z_jets_Background_Sa (07 July 2012)
#                      k-factors: https://twiki.cern.ch/twiki/pub/AtlasProtected/HiggsRecommendationsForSummer2012/8TeVCrossSections.pdf (25 July 2012)
#
#-----------------------------------------------------------------------------
ZeeNp0 = Sample( name = 'ZeeNp0', xsec = 711.77*1.23*1.0 )
ZeeNp1 = Sample( name = 'ZeeNp1', xsec = 155.17*1.23*1.0 )
ZeeNp2 = Sample( name = 'ZeeNp2', xsec = 48.745*1.23*1.0 )
ZeeNp3 = Sample( name = 'ZeeNp3', xsec = 14.225*1.23*1.0 )
ZeeNp4 = Sample( name = 'ZeeNp4', xsec = 3.7595*1.23*1.0 )
ZeeNp5 = Sample( name = 'ZeeNp5', xsec = 1.0945*1.23*1.0 )
Zee = Sample(
        name =  'Zee',
        tlatex = 'Z#rightarrow#mu#mu',
        fill_color = ROOT.kOrange+7,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        daughters = [ZeeNp0, ZeeNp1, ZeeNp2, ZeeNp3, ZeeNp4, ZeeNp5],
        )


#-----------------------------------------------------------------------------
# Zmumu
# Notes:
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#       July 25 Xsecs: AtlasProtected/TopMC12#MC12_Common_Z_jets_Background_Sa (07 July 2012)
#                      k-factors: https://twiki.cern.ch/twiki/pub/AtlasProtected/HiggsRecommendationsForSummer2012/8TeVCrossSections.pdf (25 July 2012)
#
#-----------------------------------------------------------------------------
ZmumuNp0 = Sample( name = 'ZmumuNp0', xsec = 712.11*1.23*1.0 )
ZmumuNp1 = Sample( name = 'ZmumuNp1', xsec = 154.77*1.23*1.0 )
ZmumuNp2 = Sample( name = 'ZmumuNp2', xsec = 48.912*1.23*1.0 )
ZmumuNp3 = Sample( name = 'ZmumuNp3', xsec = 14.226*1.23*1.0 )
ZmumuNp4 = Sample( name = 'ZmumuNp4', xsec = 3.7838*1.23*1.0 )
ZmumuNp5 = Sample( name = 'ZmumuNp5', xsec = 1.1148*1.23*1.0 )
Zmumu = Sample(
        name =  'Zmumu',
        tlatex = 'Z#rightarrow#mu#mu',
        fill_color = ROOT.kOrange+7,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlack,
        marker_style = 20,
        daughters = [ZmumuNp0, ZmumuNp1, ZmumuNp2, ZmumuNp3, ZmumuNp4, ZmumuNp5],
        )




#-----------------------------------------------------------------------------
# Ztautau
# Notes:
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#       July 25 Xsecs: AtlasProtected/TopMC12#MC12_Common_Z_jets_Background_Sa (07 July 2012)
#               k-factors: https://twiki.cern.ch/twiki/pub/AtlasProtected/HiggsRecommendationsForSummer2012/8TeVCrossSections.pdf (25 July 2012)
#
#-----------------------------------------------------------------------------
ZtautauNp0 = Sample( name = 'ZtautauNp0', xsec = 711.81*1.23*1.0 )
ZtautauNp1 = Sample( name = 'ZtautauNp1', xsec = 155.13*1.23*1.0 )
ZtautauNp2 = Sample( name = 'ZtautauNp2', xsec = 48.804*1.23*1.0 )
ZtautauNp3 = Sample( name = 'ZtautauNp3', xsec = 14.16*1.23*1.0 )
ZtautauNp4 = Sample( name = 'ZtautauNp4', xsec = 3.7744*1.23*1.0 )
ZtautauNp5 = Sample( name = 'ZtautauNp5', xsec = 1.1163*1.23*1.0 )
ZtautauAlpgen = Sample(
        name =  'ZtautauAlpgen',
        tlatex = 'Z#rightarrow#tau#tau',
        fill_color = ROOT.kAzure,
        line_color = ROOT.kAzure,
        marker_color = ROOT.kAzure,
        marker_style = 20,
        daughters = [ZtautauNp0, ZtautauNp1, ZtautauNp2, ZtautauNp3, ZtautauNp4, ZtautauNp5],
        )



#-----------------------------------------------------------------------------
# ttbar
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#-----------------------------------------------------------------------------
ttbar_1lep   = Sample( name = 'ttbar_1lep', xsec = 238.06*1.0*0.543 )
ttbar_allhad = Sample( name = 'ttbar_allhad', xsec = 238.06*1.0*(1.-0.543) )
ttbar = Sample(
        name =  'ttbar',
        tlatex = 't#bar{t}',
        fill_color = ROOT.kBlue+2,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kBlue+2,
        marker_style = 20,
        daughters = [ttbar_1lep, ttbar_allhad ],
        )


#-----------------------------------------------------------------------------
# single-top
#       Sept 02 Xsecs: https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/MC12A
#-----------------------------------------------------------------------------
SingleTopSChanWenu   = Sample( name = 'SingleTopSChanWenu',   xsec = 0.606*1.0*1.0  )
SingleTopSChanWmunu  = Sample( name = 'SingleTopSChanWmunu',  xsec = 0.606*1.0*1.0  )
SingleTopSChanWtaunu = Sample( name = 'SingleTopSChanWtaunu', xsec = 0.606*1.0*1.0  )
SingleTopTChane      = Sample( name = 'SingleTopTChane',      xsec = 9.48*1.0*1.0 )
SingleTopTChanmu     = Sample( name = 'SingleTopTChanmu',     xsec = 9.48*1.0*1.0 )
SingleTopTChantau    = Sample( name = 'SingleTopTChantau',    xsec = 9.48*1.0*1.0 )
SingleTopWt          = Sample( name = 'SingleTopWt',          xsec = 22.37*1.0*1.0 )
SingleTop = Sample(
        name =  'SingleTop',
        tlatex = 'Single top',
        fill_color = ROOT.kYellow+2,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kYellow+2,
        marker_style = 20,
        daughters = [SingleTopSChanWenu,SingleTopSChanWmunu,SingleTopSChanWtaunu,
                     SingleTopTChane,SingleTopTChanmu,SingleTopTChantau,
                     SingleTopWt],
        )





#-----------------------------------------------------------------------------
# diboson
# Notes:
#       Xsecs: not on twiki yet, taken from AMI (18 July 2012)
#       Xsecs (cont): Dataset search entry:
#             mc12_8TeV.105985.Herwig_AUET2CTEQ6L1_WW.evgen.EVNT.e1350
#             mc12_8TeV.105986.Herwig_AUET2CTEQ6L1_ZZ.evgen.EVNT.e1350
#             mc12_8TeV.105987.Herwig_AUET2CTEQ6L1_WZ.evgen.EVNT.e1350
#       Xsecs: twiki -- AtlasProtected/TopMC12#MC12_Common_di_Boson_samples
#
#-----------------------------------------------------------------------------

## Herwig
WW_Herwig = Sample( name = 'WW_Herwig', xsec = 3.2501E-02 * 1e3 )
ZZ_Herwig = Sample( name = 'ZZ_Herwig', xsec = 4.6914E-03 * 1e3 )
WZ_Herwig = Sample( name = 'WZ_Herwig', xsec = 1.2009E-02 * 1e3 )

diboson = Sample(
        name =  'diboson',
        tlatex = 'Diboson',
        fill_color = ROOT.kMagenta+2,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kMagenta+2,
        marker_style = 20,
        daughters = [WW_Herwig,ZZ_Herwig,WZ_Herwig],
        )

others = Sample(
        name =  'others',
        tlatex = 'Others',
        fill_color = ROOT.kYellow-8,
        line_color = ROOT.kBlack,
        marker_color = ROOT.kYellow-8,
        marker_style = 20,
        daughters = [Wenu,Wmunu,Zee,Zmumu,ttbar,diboson,SingleTop],
        )

multijet = Sample(
          name =  'Multijet',
          tlatex = 'Multijet',
          fill_color = ROOT.kGreen+2,
          line_color = ROOT.kBlack,
          marker_color = ROOT.kBlack,
          marker_style = 21, # square
          )










## set collections
mc_bkg = [Ztautau,DYtautau,ZtautauAlpgen,Wtaunu,others]

all_mc = []
all_mc += signal
all_mc += signal_rw
all_mc += mc_bkg

all_samples = all_mc + [data]





'''
gg2WW0240_WpWmenuenu
gg2WW0240_WpWmenumunu
gg2WW0240_WpWmenutaunu
gg2WW0240_WpWmmunumunu
gg2WW0240_WpWmmunuenu
gg2WW0240_WpWmmunutaunu
gg2WW0240_WpWmtaunutaunu
gg2WW0240_WpWmtaunuenu
gg2WW0240_WpWmtaunumunu
SingleTopSChanWenu
SingleTopSChanWmunu
SingleTopSChanWtaunu
SingleTopWtChanIncl
singletop_tchan_e
singletop_tchan_mu
singletop_tchan_tau
Powheg_WpWm_ee
Powheg_WpWm_me
Powheg_WpWm_te
Powheg_WpWm_em
Powheg_WpWm_mm
Powheg_WpWm_tm
Powheg_WpWm_et
Powheg_WpWm_mt
Powheg_WpWm_tt
Powheg_ZZ_4e_mll4_2pt5
Powheg_ZZ_2e2mu_mll4_2pt5
Powheg_ZZ_2e2tau_mll4_2pt5
Powheg_ZZ_4mu_mll4_2pt5
Powheg_ZZ_2mu2tau_mll4_2pt5
Powheg_ZZ_4tau_mll4_2pt5
Powheg_ZZllnunu_ee_mll4
Powheg_ZZllnunu_mm_mll4
Powheg_ZZllnunu_tt_mll4
Sherpa_Znunu
WWtaunuqq
WZtaunuqq
Zprime250tautau
Zprime500tautau
Zprime750tautau
Zprime1000tautau
Zprime1250tautau
'''













## EOF
