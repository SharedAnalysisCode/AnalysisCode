# encoding: utf-8
'''
samples.py

description:

'''

#------------------------------------------------------------------------------
# All MC xsections can be found here:
# https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/CentralMC15ProductionList
#------------------------------------------------------------------------------

## modules
from sample import Sample
import ROOT


## colors
black = ROOT.kBlack
white = ROOT.kWhite
red   = ROOT.kRed
green = ROOT.kGreen+1



#-------------------------------------------------------------------------------
# data
#-------------------------------------------------------------------------------
GRL = []

GRL += [
        #2015
        "276262","276329","276336","276416","276511","276689","276778","276790",
        "276952","276954","278880","278912","278968","279169","279259","279279",
        "279284","279345","279515","279598","279685","279813","279867","279928",
        "279932","279984","280231","280273","280319","280368","280423","280464",
        "280500","280520","280614","280673","280753","280853","280862","280950",
        "280977","281070","281074","281075","281317","281385","281411","282625",
        "282631","282712","282784","282992","283074","283155","283270","283429",
        "283608","283780","284006","284154","284213","284285","284420","284427",
        "284484",

        #2016
        "297730","298595","298609","298633","298687","298690","298771","298773",
        "298862","298967","299055","299144","299147","299184","299243","299584",
        "300279","300345","300415","300418","300487","300540","300571","300600",
        "300655","300687","300784","300800","300863","300908","301912","301918",
        "301932","301973","302053","302137","302265","302269","302300","302347",
        "302380","302391","302393","302737","302831","302872","302919","302925",
        "302956","303007","303079","303201","303208","303264","303266","303291",
        "303304","303338","303421","303499","303560","303638","303832","303846",
        "303892","303943","304006","304008","304128","304178","304198","304211",
        "304243","304308","304337","304409","304431","304494",
        ]

ds_name = '%s.physics_Main'
mc_names= 'user.gucchiel%s'

for run in GRL:
    name = ds_name % run
    globals()[name] = Sample(
            name = name,
            type = "data"
            )

list_runs =[globals()[ds_name%(run)] for run in GRL]

data = Sample(name         = "data",
              tlatex       = "Data 2015+2016",
              fill_color   = white,
              fill_style   = 0,
              line_color   = black,
              line_style   = 1,
              marker_color = black,
              marker_style = 20,
              daughters    = list_runs,
              )


#-------------------------------------------------------------------------------
# data-driven background
#-------------------------------------------------------------------------------
"""
fakes_TL = Sample( name         = 'fakes_TL',
                   tlatex       = 'Fakes TL',
                   fill_color   = ROOT.kGreen,
                   line_color   = ROOT.kGreen,
                   marker_color = ROOT.kGreen,
                   daughters    = list_runs,
                   type         = "datadriven",
                   )

fakes_LT = Sample( name         = 'fakes_LT',
                   tlatex       = 'Fakes LT',
                   fill_color   = ROOT.kBlue,
                   line_color   = ROOT.kBlue,
                   marker_color = ROOT.kBlue,
                   daughters    = list_runs,
                   type         = "datadriven",
                   )

fakes_TT = Sample( name         = 'fakes_TT',
                   tlatex       = 'Fakes TT',
                   fill_color   = ROOT.kRed,
                   line_color   = ROOT.kRed,
                   marker_color = ROOT.kRed,
                   daughters    = list_runs,
                   type         = "datadriven",
                   )

"""
fakes_cr    = Sample( name      = "fakes_cr",
                   tlatex       = "Fakes CR",
                   fill_color   = ROOT.kGray,
                   line_color   = ROOT.kGray+1,
                   line_style   = 1,
                   marker_color = ROOT.kGray+1,
                   marker_style = 20,
                   type         = "datadriven",
                   )


fakes    = Sample( name         = "fakes",
                   tlatex       = "Fakes",
                   fill_color   = ROOT.kGray,
                   line_color   = ROOT.kGray+1,
                   line_style   = 1,
                   marker_color = ROOT.kGray+1,
                   marker_style = 20,
                   #daughters    = [fakes_TL,fakes_LT,fakes_TT],
                   daughters    = list_runs,
                   type         = "datadriven",
                   )




#-----------------------------------------------------------------------------                                                                                                  
# VV (Sherpa) massed sliced samples
# Notes:                                                                                                                                                                        
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryDibosonSherpa
#-----------------------------------------------------------------------------                                         

WW_evmuv_2000M3000   = Sample( name = "Sherpa_CT10_VV_evmuv_2000M3000",  xsec =  0.000027134)
WW_muvmuv_1000M2000  = Sample( name = "Sherpa_CT10_VV_muvmuv_1000M2000",  xsec =  0.0011137)
WW_muvmuv_5000M      = Sample( name = "Sherpa_CT10_VV_muvmuv_5000M",  xsec = 1.3982e-06 )
WW_muvmuv_150M500    = Sample( name = "Sherpa_CT10_VV_muvmuv_150M500",  xsec =  0.2335)
WW_muvmuv_500M1000   = Sample( name = "Sherpa_CT10_VV_muvmuv_500M1000",  xsec =  0.0097999)
WW_evmuv_3000M4000   = Sample( name = "Sherpa_CT10_VV_evmuv_3000M4000",  xsec =  0.0000013573)
WW_muvmuv_4000M5000  = Sample( name = "Sherpa_CT10_VV_muvmuv_4000M5000",  xsec =  6.4982e-06)
WW_evev_3000M4000    = Sample( name = "Sherpa_CT10_VV_evev_3000M4000",  xsec =  2.7399e-05)
WW_evmuv_500M1000    = Sample( name = "Sherpa_CT10_VV_evmuv_500M1000",  xsec =  0.016)

WZ_lvee_4000M5000    = Sample( name = "Sherpa_CT10_VV_lvee_4000M5000",  xsec =  9.7264e-06)
WZ_lvee_500M1000     = Sample( name = "Sherpa_CT10_VV_lvee_500M1000",  xsec =  0.0060272)
WZ_lvmumu_1000M2000  = Sample( name = "Sherpa_CT10_VV_lvmumu_1000M2000",  xsec =  0.00040954)
WZ_lvmumu_3000M4000  = Sample( name = "Sherpa_CT10_VV_lvmumu_3000M4000",  xsec =  6.9018e-06)
WZ_lvee_1000M2000    = Sample( name = "Sherpa_CT10_VV_lvee_1000M2000",  xsec =  0.00027244)
WZ_lvee_3000M4000    = Sample( name = "Sherpa_CT10_VV_lvee_3000M4000",  xsec =  4.0674e-07)

ZZ_qqmumu_5000M      = Sample( name = "Sherpa_CT10_VV_qqmumu_5000M",  xsec =4.8259e-09  )  
ZZ_llmumu_5000M      = Sample( name = "Sherpa_CT10_VV_llmumu_5000M",  xsec = 6.9756e-10 )
ZZ_llmumu_150M500    = Sample( name = "Sherpa_CT10_VV_llmumu_150M500",  xsec = 0.021013 )
ZZ_llmumu_50M150     = Sample( name = "Sherpa_CT10_VV_llmumu_50M150",  xsec = 1.2263 )
ZZ_llmumu_4000M5000  = Sample( name = "Sherpa_CT10_VV_llmumu_4000M5000",  xsec = 7.6292e-09 )
ZZ_llmumu_2000M3000  = Sample( name = "Sherpa_CT10_VV_llmumu_2000M3000",  xsec =  1.6039e-06)
ZZ_llee_5000M        = Sample( name = "Sherpa_CT10_VV_llee_5000M",  xsec = 5.4441e-10 )
ZZ_qqee_2000M3000    = Sample( name = "Sherpa_CT10_VV_qqee_2000M3000",  xsec = 1.0039e-05 )
ZZ_llee_50M150       = Sample( name = "Sherpa_CT10_VV_llee_50M150",  xsec =  1.4348)

ZZ = Sample( name =   'ZZ',
                  tlatex = 'ZZ (Sherpa)',
                  fill_color = ROOT.kYellow-7,
                  line_color =  ROOT.kYellow-6,
                  marker_color =  ROOT.kYellow-6,
                  daughters = [
                                ZZ_qqmumu_5000M,
                                ZZ_llmumu_5000M,
                                ZZ_llmumu_150M500,
                                ZZ_llmumu_50M150,
                                ZZ_llmumu_4000M5000,
                                ZZ_llmumu_2000M3000,
                                ZZ_llee_5000M,
                                ZZ_qqee_2000M3000,
                                ZZ_llee_50M150,                   
                                ],
             ) 
WZ = Sample( name =   'WZ',
                  tlatex = 'WZ (Sherpa)',
                  fill_color = ROOT.kViolet+1,
                  line_color =  ROOT.kViolet+2,
                  marker_color =  ROOT.kViolet+2,
                  daughters = [
                               WZ_lvee_4000M5000,
                               WZ_lvee_500M1000,
                               WZ_lvmumu_1000M2000,
                               WZ_lvmumu_3000M4000,
                               WZ_lvee_1000M2000,
                               WZ_lvee_3000M4000,
                               ],
             )
WW = Sample( name =   'WW',
                  tlatex = 'WW (Sherpa)',
                  fill_color = ROOT.kCyan,
                  line_color =  ROOT.kCyan-1,
                  marker_color =  ROOT.kCyan-1,
                  daughters = [
                               WW_evmuv_2000M3000,
                               WW_muvmuv_1000M2000,
                               WW_muvmuv_5000M,
                               WW_muvmuv_150M500,
                               WW_muvmuv_500M1000,
                               WW_evmuv_3000M4000,
                               WW_muvmuv_4000M5000,
                               WW_evev_3000M4000,
                               WW_evmuv_500M1000,
                               ],
             )






#-----------------------------------------------------------------------------
# VV (Sherpa)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryDibosonSherpa
#-----------------------------------------------------------------------------
llll            = Sample( name = "llll",           xsec = 12.849     )
lllvSFMinus     = Sample( name = "lllvSFMinus",    xsec = 1.8442     )
lllvOFMinus     = Sample( name = "lllvOFMinus",    xsec = 3.6254     )
lllvSFPlus      = Sample( name = "lllvSFPlus",     xsec = 2.5618     )
lllvOFPlus      = Sample( name = "lllvOFPlus",     xsec = 5.0248     )
llvv            = Sample( name = "llvv",           xsec = 14.0       )
llvvjj_ss_EW4   = Sample( name = "llvvjj_ss_EW4",  xsec = 0.025797   )
llvvjj_ss_EW6   = Sample( name = "llvvjj_ss_EW6",  xsec = 0.043004   )
lllvjj_EW6      = Sample( name = "lllvjj_EW6",     xsec = 0.042017   )
lllljj_EW6      = Sample( name = "lllljj_EW6",     xsec = 0.031496   )
WplvWmqq        = Sample( name = "WplvWmqq",       xsec = 25.995     )
WpqqWmlv        = Sample( name = "WpqqWmlv",       xsec = 26.4129606 )
WlvZqq          = Sample( name = "WlvZqq",         xsec = 12.543     )
WqqZll          = Sample( name = "WqqZll",         xsec = 3.7583     )
WqqZvv          = Sample( name = "WqqZvv",         xsec = 7.4151     )
ZqqZll          = Sample( name = "ZqqZll",         xsec = 2.3645727  )
ZqqZvv          = Sample( name = "ZqqZvv",         xsec = 4.63359232 )


diboson_sherpa = Sample( name =   'diboson_sherpa',
                  tlatex = 'Di-boson (Sherpa)',
                  fill_color = ROOT.kYellow-7,
                  line_color =  ROOT.kYellow-6,
                  marker_color =  ROOT.kYellow-6,
                  daughters = [
                                llll,         
                                lllvSFMinus,  
                                lllvOFMinus,  
                                lllvSFPlus,   
                                lllvOFPlus,   
                                #llvv,          # histograms fail
                                llvvjj_ss_EW4,
                                llvvjj_ss_EW6,
                                lllvjj_EW6,   
                                lllljj_EW6,   
                                #WplvWmqq,     
                                #WpqqWmlv,     
                                #WlvZqq,       
                                #WqqZll,       
                                #WqqZvv,       
                                #ZqqZll,       
                                #ZqqZvv,
                              ],
                ) 

#-----------------------------------------------------------------------------
# VV (PowHeg)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryDibosonPowheg
#-----------------------------------------------------------------------------
WWlvlv                     = Sample( name =  "WWlvlv",                    xsec = 10.631      )
WZlvll_mll4                = Sample( name =  "WZlvll_mll4",               xsec = 4.5023      )
WZlvvv_mll4                = Sample( name =  "WZlvvv_mll4",               xsec = 2.7778      )
ZZllll_mll4                = Sample( name =  "ZZllll_mll4",               xsec = 1.2673      )
ZZvvll_mll4                = Sample( name =  "ZZvvll_mll4",               xsec = 0.91795     )
ZZvvvv_mll4                = Sample( name =  "ZZvvvv_mll4",               xsec = 0.54901     )
WWlvqq                     = Sample( name =  "WWlvqq",                    xsec = 44.18       )
WZqqll_mll20               = Sample( name =  "WZqqll_mll20",              xsec = 3.2777      )
WZqqvv                     = Sample( name =  "WZqqvv",                    xsec = 5.7576      )
WZlvqq_mqq20               = Sample( name =  "WZlvqq_mqq20",              xsec = 10.086      )
ZZvvqq_mqq20               = Sample( name =  "ZZvvqq_mqq20",              xsec = 3.9422      )
ZZqqll_mqq20mll20          = Sample( name =  "ZZqqll_mqq20mll20",         xsec = 2.2699      )
ZZllll_mll4_m4l_500_13000  = Sample( name =  "ZZllll_mll4_m4l_500_13000", xsec = 0.004658938 )

diboson_powheg = Sample( name =   'diboson_powheg',
                  tlatex = 'Di-boson (Powheg)',
                  fill_color = ROOT.kYellow-7,
                  line_color =  ROOT.kYellow-6,
                  marker_color =  ROOT.kYellow-6,
                  daughters = [
                                WWlvlv,                   
                                WZlvll_mll4,              
                                WZlvvv_mll4,              
                                ZZllll_mll4,              
                                ZZvvll_mll4,              
                                ZZvvvv_mll4,              
                                WWlvqq,                   
                                WZqqll_mll20,             
                                WZqqvv,                   
                                WZlvqq_mqq20,             
                                ZZvvqq_mqq20,             
                                #ZZqqll_mqq20mll20,        
                                #ZZllll_mll4_m4l_500_13000,
                              ],
                ) 


#-----------------------------------------------------------------------------
# W + jets (Sherpa 2.2)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsSherpa22Light (light filter)
#                         https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsSherpa22C     (C filter) 
#                         https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsSherpa22B     (B filter) 
#-----------------------------------------------------------------------------

#-----
# Wenu
#-----

Wenu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt0_70_CVetoBVeto",         xsec = 15813.6777927 ) 
Wenu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt70_140_CVetoBVeto",       xsec = 376.41531567  )
Wenu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt140_280_CVetoBVeto",      xsec = 50.191601517  )
Wenu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt280_500_CVetoBVeto",      xsec = 3.43565825    )
Wenu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt500_700_CVetoBVeto",      xsec = 0.211528021   )
Wenu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt700_1000_CVetoBVeto",     xsec = 0.036964172   )
Wenu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt1000_2000_CVetoBVeto",    xsec = 0.004645048   )
Wenu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt2000_E_CMS_CVetoBVeto",   xsec = 1.2973e-05    )
                                                                                                             
Wenu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt0_70_CFilterBVeto",       xsec =  2684.61495225 )
Wenu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt70_140_CFilterBVeto",     xsec =  146.400460335 )
Wenu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt140_280_CFilterBVeto",    xsec =  22.599123229  )
Wenu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt280_500_CFilterBVeto",    xsec =  1.680719916   )
Wenu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt500_700_CFilterBVeto",    xsec =  0.107245951   )
Wenu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt700_1000_CFilterBVeto",   xsec =  0.019023648   )
Wenu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt1000_2000_CFilterBVeto",  xsec =  0.002444187   )
Wenu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt2000_E_CMS_CFilterBVeto", xsec =  2.364e-06     )
                                                                                                             
Wenu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt0_70_BFilter",            xsec =  912.150989719)
Wenu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt70_140_BFilter",          xsec =  49.376826267 )
Wenu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt140_280_BFilter",         xsec =  8.635509901  )
Wenu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt280_500_BFilter",         xsec =  0.729320539  )
Wenu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt500_700_BFilter",         xsec =  0.051038517  )
Wenu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt700_1000_BFilter",        xsec =  0.00948474   )
Wenu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt1000_2000_BFilter",       xsec =  0.001307192  )
Wenu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Wenu_Pt2000_E_CMS_BFilter",      xsec =  3.705e-06    )


Wenu = Sample( name =   'Wenu',
                  tlatex = 'W #rightarrow e#nu+jets',
                  fill_color = ROOT.kRed+1,
                  line_color =  ROOT.kRed+2,
                  marker_color =  ROOT.kRed+2,
                  daughters = [
                               Wenu_Pt0_70_CVetoBVeto,        
                               Wenu_Pt70_140_CVetoBVeto,                                    
                               Wenu_Pt140_280_CVetoBVeto,     
                               Wenu_Pt280_500_CVetoBVeto,     
                               Wenu_Pt500_700_CVetoBVeto,     
                               Wenu_Pt700_1000_CVetoBVeto,    
                               Wenu_Pt1000_2000_CVetoBVeto,   
                               Wenu_Pt2000_E_CMS_CVetoBVeto,  
                               Wenu_Pt0_70_CFilterBVeto,      
                               Wenu_Pt70_140_CFilterBVeto,    
                               Wenu_Pt140_280_CFilterBVeto,   
                               Wenu_Pt280_500_CFilterBVeto,   
                               Wenu_Pt500_700_CFilterBVeto,   
                               Wenu_Pt700_1000_CFilterBVeto,  
                               Wenu_Pt1000_2000_CFilterBVeto, 
                               Wenu_Pt2000_E_CMS_CFilterBVeto,
                               Wenu_Pt0_70_BFilter,           
                               Wenu_Pt70_140_BFilter,         
                               Wenu_Pt140_280_BFilter,        
                               Wenu_Pt280_500_BFilter,        
                               Wenu_Pt500_700_BFilter,        
                               Wenu_Pt700_1000_BFilter,       
                               Wenu_Pt1000_2000_BFilter,      
                               Wenu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 


#------
# Wmunu
#------

Wmunu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt0_70_CVetoBVeto",         xsec =  15795.1948618)
Wmunu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt70_140_CVetoBVeto",       xsec =  377.749548487) 
Wmunu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt140_280_CVetoBVeto",      xsec =  50.151421849 )
Wmunu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt280_500_CVetoBVeto",      xsec =  3.533801265  )
Wmunu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt500_700_CVetoBVeto",      xsec =  0.213331248  )
Wmunu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt700_1000_CVetoBVeto",     xsec =  0.037111165  )
Wmunu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt1000_2000_CVetoBVeto",    xsec =  0.00478857   )
Wmunu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt2000_E_CMS_CVetoBVeto",   xsec =  1.2348e-05   )
                                                                                                               
Wmunu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt0_70_CFilterBVeto",       xsec = 2675.17332482 )
Wmunu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt70_140_CFilterBVeto",     xsec = 145.131941493 )
Wmunu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt140_280_CFilterBVeto",    xsec = 22.576834194  )
Wmunu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt280_500_CFilterBVeto",    xsec = 1.686521076   )
Wmunu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt500_700_CFilterBVeto",    xsec = 0.107132134   )
Wmunu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt700_1000_CFilterBVeto",   xsec = 0.018196255   )
Wmunu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt1000_2000_CFilterBVeto",  xsec = 0.002494854   )
Wmunu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt2000_E_CMS_CFilterBVeto", xsec = 9.812e-06     )
                                                                                                               
Wmunu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt0_70_BFilter",            xsec = 907.616822112 )
Wmunu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt70_140_BFilter",          xsec = 49.37500785   )
Wmunu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt140_280_BFilter",         xsec = 8.640805039   )
Wmunu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt280_500_BFilter",         xsec = 0.732282814   )
Wmunu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt500_700_BFilter",         xsec = 0.050487154   )
Wmunu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt700_1000_BFilter",        xsec = 0.009428206   )
Wmunu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt1000_2000_BFilter",       xsec = 0.001284408   )
Wmunu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Wmunu_Pt2000_E_CMS_BFilter",      xsec = 5.314e-06     )

Wmunu = Sample( name =   'Wmunu',
                  tlatex = 'W #rightarrow #mu#nu+jets',
                  fill_color = ROOT.kGreen+1,
                  line_color =  ROOT.kGreen+2,
                  marker_color =  ROOT.kGreen+2,
                  daughters = [
                               Wmunu_Pt0_70_CVetoBVeto,        
                               Wmunu_Pt70_140_CVetoBVeto,                                    
                               Wmunu_Pt140_280_CVetoBVeto,     
                               Wmunu_Pt280_500_CVetoBVeto,     
                               Wmunu_Pt500_700_CVetoBVeto,     
                               Wmunu_Pt700_1000_CVetoBVeto,    
                               Wmunu_Pt1000_2000_CVetoBVeto,   
                               Wmunu_Pt2000_E_CMS_CVetoBVeto,  
                               Wmunu_Pt0_70_CFilterBVeto,      
                               Wmunu_Pt70_140_CFilterBVeto,    
                               Wmunu_Pt140_280_CFilterBVeto,   
                               Wmunu_Pt280_500_CFilterBVeto,   
                               Wmunu_Pt500_700_CFilterBVeto,   
                               Wmunu_Pt700_1000_CFilterBVeto,  
                               Wmunu_Pt1000_2000_CFilterBVeto, 
                               Wmunu_Pt2000_E_CMS_CFilterBVeto,
                               Wmunu_Pt0_70_BFilter,           
                               Wmunu_Pt70_140_BFilter,         
                               Wmunu_Pt140_280_BFilter,        
                               Wmunu_Pt280_500_BFilter,        
                               Wmunu_Pt500_700_BFilter,        
                               Wmunu_Pt700_1000_BFilter,       
                               Wmunu_Pt1000_2000_BFilter,      
                               Wmunu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 

#-------
# Wtaunu
#-------

Wtaunu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt0_70_CVetoBVeto",         xsec = 15821.9692868 )
Wtaunu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt70_140_CVetoBVeto",       xsec = 375.759077047 ) 
Wtaunu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt140_280_CVetoBVeto",      xsec = 50.173358226  )
Wtaunu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt280_500_CVetoBVeto",      xsec = 3.450438494   )
Wtaunu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt500_700_CVetoBVeto",      xsec = 0.209886778   )
Wtaunu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt700_1000_CVetoBVeto",     xsec = 0.039884689   )
Wtaunu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt1000_2000_CVetoBVeto",    xsec = 0.004868065   )
Wtaunu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt2000_E_CMS_CVetoBVeto",   xsec = 1.4245e-05    )
                                                                                                                 
Wtaunu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt0_70_CFilterBVeto",       xsec = 2683.83259267)
Wtaunu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt70_140_CFilterBVeto",     xsec = 144.539591316)
Wtaunu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt140_280_CFilterBVeto",    xsec = 22.558816959 )
Wtaunu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt280_500_CFilterBVeto",    xsec = 1.687956502  )
Wtaunu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt500_700_CFilterBVeto",    xsec = 0.108804181  )
Wtaunu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt700_1000_CFilterBVeto",   xsec = 0.01927425   )
Wtaunu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt1000_2000_CFilterBVeto",  xsec = 0.00251029   )
Wtaunu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt2000_E_CMS_CFilterBVeto", xsec = 8.707e-06    )
                                                                                                                 
Wtaunu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt0_70_BFilter",            xsec = 909.56502252)
Wtaunu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt70_140_BFilter",          xsec = 49.107324606)
Wtaunu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt140_280_BFilter",         xsec = 8.611129318 )
Wtaunu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt280_500_BFilter",         xsec = 0.711433732 )
Wtaunu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt500_700_BFilter",         xsec = 0.048001365 )
Wtaunu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt700_1000_BFilter",        xsec = 0.009455976 )
Wtaunu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt1000_2000_BFilter",       xsec = 0.001236195 )
Wtaunu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Wtaunu_Pt2000_E_CMS_BFilter",      xsec = 5.143e-06   )

Wtaunu = Sample( name =   'Wtaunu',
                  tlatex = 'W #rightarrow #tau#nu+jets',
                  fill_color = ROOT.kBlue+1,
                  line_color =  ROOT.kBlue+2,
                  marker_color =  ROOT.kBlue+2,
                  daughters = [
                               Wtaunu_Pt0_70_CVetoBVeto,        
                               Wtaunu_Pt70_140_CVetoBVeto,                                    
                               Wtaunu_Pt140_280_CVetoBVeto,     
                               Wtaunu_Pt280_500_CVetoBVeto,     
                               Wtaunu_Pt500_700_CVetoBVeto,     
                               Wtaunu_Pt700_1000_CVetoBVeto,    
                               Wtaunu_Pt1000_2000_CVetoBVeto,   
                               Wtaunu_Pt2000_E_CMS_CVetoBVeto,  
                               Wtaunu_Pt0_70_CFilterBVeto,      
                               Wtaunu_Pt70_140_CFilterBVeto,    
                               Wtaunu_Pt140_280_CFilterBVeto,   
                               Wtaunu_Pt280_500_CFilterBVeto,   
                               Wtaunu_Pt500_700_CFilterBVeto,   
                               Wtaunu_Pt700_1000_CFilterBVeto,  
                               Wtaunu_Pt1000_2000_CFilterBVeto, 
                               Wtaunu_Pt2000_E_CMS_CFilterBVeto,
                               Wtaunu_Pt0_70_BFilter,           
                               Wtaunu_Pt70_140_BFilter,         
                               Wtaunu_Pt140_280_BFilter,        
                               Wtaunu_Pt280_500_BFilter,        
                               Wtaunu_Pt500_700_BFilter,        
                               Wtaunu_Pt700_1000_BFilter,       
                               Wtaunu_Pt1000_2000_BFilter,      
                               Wtaunu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 







#-----------------------------------------------------------------------------
# W + jets (Powheg)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryWjetsPowPy8Incl
#                         
#-----------------------------------------------------------------------------
Wplusenu     = Sample( name =  "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wplusenu",     xsec = 11500.9154 ) 
Wminusenu    = Sample( name =  "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wminusenu",    xsec = 8579.0011  ) 
                                                                                                         
Wplusmunu    = Sample( name =  "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wplusmunu",    xsec = 11500.9154 ) 
Wminusmunu   = Sample( name =  "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wminusmunu",   xsec = 8579.0011  ) 

Wplustaunu   = Sample( name =  "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wplustaunu",   xsec = 11500.9154 ) 
Wminustaunu  = Sample( name =  "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Wminustaunu",  xsec = 8579.0011  ) 


WenuPowheg = Sample( name =   'WenuPowheg',
                  tlatex = 'W #rightarrow e#nu+jets (Powheg)',
                  fill_color = ROOT.kRed+1,
                  line_color =  ROOT.kRed+2,
                  marker_color =  ROOT.kRed+2,
                  daughters = [
                               Wplusenu,        
                               Wminusenu,                                    
                              ],
                ) 


WmunuPowheg = Sample( name =   'WmunuPowheg',
                  tlatex = 'W #rightarrow #mu#nu+jets (Powheg)',
                  fill_color = ROOT.kGreen+1,
                  line_color =  ROOT.kGreen+2,
                  marker_color =  ROOT.kGreen+2,
                  daughters = [
                               Wplusmunu,        
                               Wminusmunu,                                    
                              ],
                ) 


WtaunuPowheg = Sample( name =   'WtaunuPowheg',
                  tlatex = 'W #rightarrow #tau#nu+jets (Powheg)',
                  fill_color = ROOT.kBlue+1,
                  line_color =  ROOT.kBlue+2,
                  marker_color =  ROOT.kBlue+2,
                  daughters = [
                               Wplustaunu,        
                               Wminustaunu,                                    
                              ],
                ) 


#-----------------------------------------------------------------------------
# Z + jets (Powheg)
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsPowPy8Incl
#                         
#-----------------------------------------------------------------------------

ZeePP       = Sample( name  = "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zee",     xsec = 1950.6321 ) 
ZmumuPP     = Sample( name  = "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Zmumu",   xsec = 1950.6321 ) 
ZtautauPP   = Sample( name  = "PowhegPythia8EvtGen_AZNLOCTEQ6L1_Ztautau", xsec = 1950.6321 ) 


ZeePowheg       = Sample( name         = "ZeePowheg",     
                          tlatex       = 'Z #rightarrow ee+jets',
                          fill_color   =  ROOT.kOrange+1,
                          line_color   =  ROOT.kOrange+2,
                          marker_color =  ROOT.kOrange+2,
                          daughters = [
                               ZeePP,     
                              ],
                  ) 


ZmumuPowheg     = Sample( name         = "ZmumuPowheg",   
                          tlatex       = 'Z #rightarrow #mu#mu+jets',
                          fill_color   = ROOT.kSpring+1,
                          line_color   = ROOT.kSpring+2,
                          marker_color = ROOT.kSpring+2,
                          daughters = [
                               ZmumuPP,     
                              ],
                  ) 


ZtautauPowheg   = Sample( name         = "ZtautauPowheg", 
                          tlatex       = 'Z #rightarrow #tau#tau+jets',
                          fill_color   = ROOT.kAzure-4,
                          line_color   = ROOT.kAzure-5,
                          marker_color = ROOT.kAzure-5,
                          daughters = [
                               ZtautauPP,     
                              ],
                  ) 


#-----------------------------------------------------------------------------
# Z + jets (Sherpa 2.2)
# Notes:
#       * cross sections:  https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsSherpa22Light (light filter)
#                          https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsSherpa22C     (C filter) 
#                          https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryZjetsSherpa22B     (B filter) 
# for my tags!!!
# https://twiki.cern.ch/twiki/pub/AtlasProtected/CentralMC15ProductionList/XSections_13TeV_e3651_e4133.txt
#-----------------------------------------------------------------------------

#-----
# Zee
#-----

Zee_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt0_70_CVetoBVeto",                xsec = 1641.4628707  ) 
Zee_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt70_140_CVetoBVeto",              xsec = 46.790575075  )
Zee_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt140_280_CVetoBVeto",             xsec = 6.789837772   )
Zee_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt280_500_CVetoBVeto",             xsec = 0.48716142    )
Zee_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt500_700_CVetoBVeto",             xsec = 0.02875511    )
Zee_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt700_1000_CVetoBVeto",            xsec = 0.005414517   )
Zee_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt1000_2000_CVetoBVeto",           xsec = 0.000697776   )
Zee_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt2000_E_CMS_CVetoBVeto",          xsec = 2.524e-06     ) 
                                                                                                         
Zee_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt0_70_CFilterBVeto",              xsec = 241.466440999 )
Zee_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt70_140_CFilterBVeto",            xsec = 14.049268454  )
Zee_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt140_280_CFilterBVeto",           xsec = 2.42660918    )
Zee_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt280_500_CFilterBVeto",           xsec = 0.198314112   )
Zee_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt500_700_CFilterBVeto",           xsec = 0.012936803   )
Zee_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt700_1000_CFilterBVeto",          xsec = 0.002400844   )
Zee_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt1000_2000_CFilterBVeto",         xsec = 0.00033278    )
Zee_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt2000_E_CMS_CFilterBVeto",        xsec = 1.218e-06     )
                                                                                                         
Zee_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt0_70_BFilter",                   xsec = 140.517436867 )
Zee_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt70_140_BFilter",                 xsec = 8.850204229   )
Zee_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt140_280_BFilter",                xsec = 1.558081087   )
Zee_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt280_500_BFilter",                xsec = 0.123000982   )
Zee_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt500_700_BFilter",                xsec = 0.007968854   )
Zee_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt700_1000_BFilter",               xsec = 0.001494724   )
Zee_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt1000_2000_BFilter",              xsec = 0.000189395   )
Zee_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Zee_Pt2000_E_CMS_BFilter",             xsec = 6.99e-07      )

Zee = Sample( name =   'Zee',
                  tlatex = 'Z #rightarrow ee+jets',
                  fill_color = ROOT.kOrange+1,
                  line_color =  ROOT.kOrange+2,
                  marker_color =  ROOT.kOrange+2,
                  daughters = [
                               Zee_Pt0_70_CVetoBVeto,        
                               Zee_Pt70_140_CVetoBVeto,                                    
                               Zee_Pt140_280_CVetoBVeto,     
                               Zee_Pt280_500_CVetoBVeto,     
                               Zee_Pt500_700_CVetoBVeto,     
                               Zee_Pt700_1000_CVetoBVeto,    
                               Zee_Pt1000_2000_CVetoBVeto,   
                               Zee_Pt2000_E_CMS_CVetoBVeto,  
                               Zee_Pt0_70_CFilterBVeto,      
                               Zee_Pt70_140_CFilterBVeto,    
                               Zee_Pt140_280_CFilterBVeto,   
                               Zee_Pt280_500_CFilterBVeto,   
                               Zee_Pt500_700_CFilterBVeto,   
                               Zee_Pt700_1000_CFilterBVeto,  
                               Zee_Pt1000_2000_CFilterBVeto, 
                               Zee_Pt2000_E_CMS_CFilterBVeto,
                               Zee_Pt0_70_BFilter,           
                               Zee_Pt70_140_BFilter,         
                               Zee_Pt140_280_BFilter,        
                               Zee_Pt280_500_BFilter,        
                               Zee_Pt500_700_BFilter,        
                               Zee_Pt700_1000_BFilter,       
                               Zee_Pt1000_2000_BFilter,      
                               Zee_Pt2000_E_CMS_BFilter,     
                              ],
                ) 


#-------
# Zmumu
#-------

Zmumu_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_CVetoBVeto",              xsec = 1642.54477535  )
Zmumu_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_CVetoBVeto",            xsec = 46.639099307   ) 
Zmumu_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt140_280_CVetoBVeto",           xsec = 6.776899365    )
Zmumu_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt280_500_CVetoBVeto",           xsec = 0.481671305    )
Zmumu_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_CVetoBVeto",           xsec = 0.030237082    )
Zmumu_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt700_1000_CVetoBVeto",          xsec = 0.005363995    )
Zmumu_Pt1000_2000_CVetoBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt1000_2000_CVetoBVeto",         xsec = 0.00069072     )
Zmumu_Pt2000_E_CMS_CVetoBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt2000_E_CMS_CVetoBVeto",        xsec = 2.451e-06      )
                                                                                                        
Zmumu_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_CFilterBVeto",            xsec = 240.030832472  )
Zmumu_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_CFilterBVeto",          xsec = 14.009508576   )
Zmumu_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt140_280_CFilterBVeto",         xsec = 2.407495134    )
Zmumu_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt280_500_CFilterBVeto",         xsec = 0.195283767    )
Zmumu_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_CFilterBVeto",         xsec = 0.01296887     )
Zmumu_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt700_1000_CFilterBVeto",        xsec = 0.002371048    )
Zmumu_Pt1000_2000_CFilterBVeto  = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt1000_2000_CFilterBVeto",       xsec = 0.000318973    )
Zmumu_Pt2000_E_CMS_CFilterBVeto = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt2000_E_CMS_CFilterBVeto",      xsec = 1.38e-06       )
                                                                                                        
Zmumu_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt0_70_BFilter",                 xsec = 142.586650552  )
Zmumu_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt70_140_BFilter",               xsec = 8.955685233    )
Zmumu_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt140_280_BFilter",              xsec = 1.561047731    )
Zmumu_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt280_500_BFilter",              xsec = 0.123565964    )
Zmumu_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt500_700_BFilter",              xsec = 0.007654784    )
Zmumu_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt700_1000_BFilter",             xsec = 0.001495305    )
Zmumu_Pt1000_2000_BFilter       = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt1000_2000_BFilter",            xsec = 0.000184686    )
Zmumu_Pt2000_E_CMS_BFilter      = Sample( name =  "Sherpa_NNPDF30NNLO_Zmumu_Pt2000_E_CMS_BFilter",           xsec = 6.69e-07       )

Zmumu = Sample( name =   'Zmumu',
                  tlatex = 'Z #rightarrow #mu#mu+jets',
                  fill_color = ROOT.kSpring+1,
                  line_color =  ROOT.kSpring+2,
                  marker_color =  ROOT.kSpring+2,
                  daughters = [
                               Zmumu_Pt0_70_CVetoBVeto,        
                               Zmumu_Pt70_140_CVetoBVeto,                                    
                               Zmumu_Pt140_280_CVetoBVeto,     
                               Zmumu_Pt280_500_CVetoBVeto,     
                               Zmumu_Pt500_700_CVetoBVeto,     
                               Zmumu_Pt700_1000_CVetoBVeto,    
                               Zmumu_Pt1000_2000_CVetoBVeto,   
                               Zmumu_Pt2000_E_CMS_CVetoBVeto,  
                               Zmumu_Pt0_70_CFilterBVeto,      
                               Zmumu_Pt70_140_CFilterBVeto,    
                               Zmumu_Pt140_280_CFilterBVeto,   
                               Zmumu_Pt280_500_CFilterBVeto,   
                               Zmumu_Pt500_700_CFilterBVeto,   
                               Zmumu_Pt700_1000_CFilterBVeto,  
                               Zmumu_Pt1000_2000_CFilterBVeto, 
                               Zmumu_Pt2000_E_CMS_CFilterBVeto,
                               Zmumu_Pt0_70_BFilter,           
                               Zmumu_Pt70_140_BFilter,         
                               Zmumu_Pt140_280_BFilter,        
                               Zmumu_Pt280_500_BFilter,        
                               Zmumu_Pt500_700_BFilter,        
                               Zmumu_Pt700_1000_BFilter,       
                               Zmumu_Pt1000_2000_BFilter,      
                               Zmumu_Pt2000_E_CMS_BFilter,     
                              ],
                ) 

#---------
# Ztautau
#---------

Ztautau_Pt0_70_CVetoBVeto         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt0_70_CVetoBVeto",         xsec = 1643.85019048 )
Ztautau_Pt70_140_CVetoBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt70_140_CVetoBVeto",       xsec = 6.73378408    ) 
Ztautau_Pt140_280_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt140_280_CVetoBVeto",      xsec = 0.486837566   )
Ztautau_Pt280_500_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt280_500_CVetoBVeto",      xsec = 0.030084735   )
Ztautau_Pt500_700_CVetoBVeto      = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt500_700_CVetoBVeto",      xsec = 0.005386908   )
Ztautau_Pt700_1000_CVetoBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt700_1000_CVetoBVeto",     xsec = 0.0006955     )
                                                                                                        
Ztautau_Pt0_70_CFilterBVeto       = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt0_70_CFilterBVeto",       xsec = 240.97383023 )
Ztautau_Pt70_140_CFilterBVeto     = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt70_140_CFilterBVeto",     xsec = 14.026868379 )
Ztautau_Pt140_280_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt140_280_CFilterBVeto",    xsec = 2.413076391  )
Ztautau_Pt280_500_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt280_500_CFilterBVeto",    xsec = 0.196832713  )
Ztautau_Pt500_700_CFilterBVeto    = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt500_700_CFilterBVeto",    xsec = 0.013210254  )
Ztautau_Pt700_1000_CFilterBVeto   = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt700_1000_CFilterBVeto",   xsec = 0.002395235  )
                                                                                                        
Ztautau_Pt0_70_BFilter            = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt0_70_BFilter",            xsec = 140.512238804 )
Ztautau_Pt70_140_BFilter          = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt70_140_BFilter",          xsec = 8.832529157   )
Ztautau_Pt140_280_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt140_280_BFilter",         xsec = 1.555402702   )
Ztautau_Pt280_500_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt280_500_BFilter",         xsec = 0.124324067   )
Ztautau_Pt500_700_BFilter         = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt500_700_BFilter",         xsec = 0.008163159   )
Ztautau_Pt700_1000_BFilter        = Sample( name =  "Sherpa_NNPDF30NNLO_Ztautau_Pt700_1000_BFilter",        xsec = 0.001473957   )


Ztautau = Sample( name =   'Ztautau',
                  tlatex = 'Z #rightarrow #tau#tau+jets',
                  fill_color = ROOT.kAzure-4,
                  line_color =  ROOT.kAzure-5,
                  marker_color =  ROOT.kAzure-5,
                  daughters = [
                               Ztautau_Pt0_70_CVetoBVeto,        
                               Ztautau_Pt70_140_CVetoBVeto,                                    
                               Ztautau_Pt140_280_CVetoBVeto,     
                               Ztautau_Pt280_500_CVetoBVeto,     
                               Ztautau_Pt500_700_CVetoBVeto,     
                               Ztautau_Pt700_1000_CVetoBVeto,    
                               Ztautau_Pt0_70_CFilterBVeto,      
                               Ztautau_Pt70_140_CFilterBVeto,    
                               Ztautau_Pt140_280_CFilterBVeto,   
                               Ztautau_Pt280_500_CFilterBVeto,   
                               Ztautau_Pt500_700_CFilterBVeto,   
                               Ztautau_Pt700_1000_CFilterBVeto,  
                               Ztautau_Pt0_70_BFilter,           
                               Ztautau_Pt70_140_BFilter,         
                               Ztautau_Pt140_280_BFilter,        
                               Ztautau_Pt280_500_BFilter,   
                               Ztautau_Pt500_700_BFilter,        
                               Ztautau_Pt700_1000_BFilter,       
                              ],
                ) 


#-----------------------------------------------------------------------------
# Top 
#-----------------------------------------------------------------------------

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ttX 
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbarX
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ttW_Np0                               = Sample( name =  "ttW_Np0",        xsec =  0.17656    )  
ttW_Np1                               = Sample( name =  "ttW_Np1",        xsec =  0.14062    ) 
ttW_Np2                               = Sample( name =  "ttW_Np2",        xsec =  0.1368     )
ttZnnqq_Np0                           = Sample( name =  "ttZnnqq_Np0",    xsec =  0.11122    )
ttZnnqq_Np1                           = Sample( name =  "ttZnnqq_Np1",    xsec =  0.095466   )
ttZnnqq_Np2                           = Sample( name =  "ttZnnqq_Np2",    xsec =  0.10512    )
ttee_Np0                              = Sample( name =  "ttee_Np0",       xsec =  0.0088155  )
ttee_Np1                              = Sample( name =  "ttee_Np1",       xsec =  0.01438    )
ttmumu_Np0                            = Sample( name =  "ttmumu_Np0",     xsec =  0.0088422  )                         
ttmumu_Np1                            = Sample( name =  "ttmumu_Np1",     xsec =  0.014375   )
tttautau_Np0                          = Sample( name =  "tttautau_Np0",   xsec =  0.0090148  )
tttautau_Np1                          = Sample( name =  "tttautau_Np1",   xsec =  0.014636   )

ttX = Sample( name =   'ttX',
                  tlatex = 'ttX',
                  fill_color = ROOT.kViolet+1,
                  line_color =  ROOT.kViolet+2,
                  marker_color =  ROOT.kViolet+2,
                  daughters = [
                               ttW_Np0,                
                               ttW_Np1,        
                               ttW_Np2,        
                               ttZnnqq_Np0,    
                               ttZnnqq_Np1,    
                               ttZnnqq_Np2,    
                               ttee_Np0,       
                               ttee_Np1,       
                               ttmumu_Np0,     
                               ttmumu_Np1,     
                               tttautau_Np0,   
                               tttautau_Np1,   
                              ],
                ) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# single-top
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummarySingleTop
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#SingleTopSchan_noAllHad_top           = Sample( name =  "SingleTopSchan_noAllHad_top",       xsec =  2.0517 )
#SingleTopSchan_noAllHad_antitop       = Sample( name =  "SingleTopSchan_noAllHad_antitop",   xsec =  1.2615 )
#singletop_tchan_lept_top              = Sample( name =  "singletop_tchan_lept_top",          xsec =  43.739 )
#singletop_tchan_lept_antitop          = Sample( name =  "singletop_tchan_lept_antitop",      xsec =  25.778 )
Wt_inclusive_top                      = Sample( name =  "Wt_inclusive_top",                  xsec =  34.009 ) 
Wt_inclusive_antitop                  = Sample( name =  "Wt_inclusive_antitop",              xsec =  33.989 )
"""
singletop = Sample( name =   'singletop',
                    tlatex = 'single-top',
                    fill_color = ROOT.kRed+3,
                    line_color =  ROOT.kRed+4,
                    marker_color =  ROOT.kRed+4,
                    daughters = [
                                 SingleTopSchan_noAllHad_top,    
                                 SingleTopSchan_noAllHad_antitop,
                                 singletop_tchan_lept_top,       
                                 singletop_tchan_lept_antitop,   
                                 Wt_inclusive_top,               
                                 Wt_inclusive_antitop,           
                                ],
                ) 
"""
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ttbar bulk samples
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbar 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ttbar_hdamp172p5_nonallhad            = Sample( name =  "ttbar_hdamp172p5_nonallhad", xsec = 451.645679998 )
ttbar_hdamp172p5_allhad               = Sample( name =  "ttbar_hdamp172p5_allhad",    xsec = 380.11432     )
ttbar_nonallhad                       = Sample( name =  "ttbar_nonallhad",            xsec = 451.645680001 )

ttbar_dilep = Sample( name = "PowhegPythiaEvtGen_P2012_ttbar_hdamp172p5_dil" , xsec = 87.627231743)

ttbar = Sample( name =  'ttbar_dilep',
                    tlatex = 'ttbar_dilep',
                    fill_color = ROOT.kCyan+1,
                    line_color =  ROOT.kCyan+2,
                    marker_color =  ROOT.kCyan+2,
                    daughters = [
                                 #ttbar_hdamp172p5_nonallhad,
                                 #ttbar_hdamp172p5_allhad,   
                                 #ttbar_nonallhad,           
                                 ttbar_dilep,
                                ],
                ) 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ttbar sliced samples
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryTTbarSliced 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ttbar_hdamp172p5_nonallhad_mtt_1      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_1",  xsec = 3.926242464   )
ttbar_hdamp172p5_nonallhad_mtt_2      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_2",  xsec = 1.617309099   )                         
ttbar_hdamp172p5_nonallhad_mtt_3      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_3",  xsec = 0.718018025   )
ttbar_hdamp172p5_nonallhad_mtt_4      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_4",  xsec = 0.431858588   )
ttbar_hdamp172p5_nonallhad_mtt_5      = Sample( name =  "ttbar_hdamp172p5_nonallhad_mtt_5",  xsec = 0.25723035    )
ttbarHT6c_1k_hdamp172p5_nonAH         = Sample( name =  "ttbarHT6c_1k_hdamp172p5_nonAH",     xsec = 19.068284245  )
ttbarHT1k_1k5_hdamp172p5_nonAH        = Sample( name =  "ttbarHT1k_1k5_hdamp172p5_nonAH",    xsec = 2.665728834   )
ttbarHT1k5_hdamp172p5_nonAH           = Sample( name =  "ttbarHT1k5_hdamp172p5_nonAH",       xsec = 0.470232424   )
ttbarMET200_hdamp172p5_nonAH          = Sample( name =  "ttbarMET200_hdamp172p5_nonAH",      xsec = 7.669803669   )
ttbar_hdamp345_down_nonallhad         = Sample( name =  "ttbar_hdamp345_down_nonallhad",     xsec = 451.645679999 ) 
ttbar_hdamp172_up_nonallhad           = Sample( name =  "ttbar_hdamp172_up_nonallhad",       xsec = 451.64568     )
ttbar_hdamp172p5_nonallhad            = Sample( name =  "ttbar_hdamp172p5_nonallhad",        xsec = 451.645679998 )


ttbar_slices = Sample( name =  'ttbar_slices',
                    tlatex = 'ttbar',
                    fill_color = ROOT.kCyan+1,
                    line_color =  ROOT.kCyan+2,
                    marker_color =  ROOT.kCyan+2,
                    daughters = [
                                 #ttbar_hdamp172p5_nonallhad_mtt_1,
                                 #ttbar_hdamp172p5_nonallhad_mtt_2,
                                 #ttbar_hdamp172p5_nonallhad_mtt_3,
                                 #ttbar_hdamp172p5_nonallhad_mtt_4,
                                 #ttbar_hdamp172p5_nonallhad_mtt_5,
                                 
                                 #ttbarHT6c_1k_hdamp172p5_nonAH,   
                                 #ttbarHT1k_1k5_hdamp172p5_nonAH,  
                                 #ttbarHT1k5_hdamp172p5_nonAH,     
                                 #ttbarMET200_hdamp172p5_nonAH,    
                                 
                                 #ttbar_hdamp345_down_nonallhad,   
                                 #ttbar_hdamp172_up_nonallhad,     
                                 #ttbar_hdamp172p5_nonallhad,      #just use this one!
                                ],
                ) 

#-----------------------------------------------------------------------------
# Doubly charged Higss 
# Notes:
#       * cross sections: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/XsecSummaryHiggsBSMOthers 
#-----------------------------------------------------------------------------

DCH_name =  'DCH%d'
DCH_tlatex = 'm_{H^{\pm\pm}}=%d GeV'
DCH_masses = [
    300,
    400,
    500,
    600,
    700,
    800,
    900,
    1000,
    1100,
    1200,
    1300,
    ]

for m in DCH_masses:
    name = DCH_name % m
    globals()[name] = Sample(
            name = name,
            tlatex = DCH_tlatex % (m),
            line_color = ROOT.kOrange-3,
            marker_color = ROOT.kOrange-3,
            fill_color = ROOT.kOrange-3,
            line_width  = 3,
            line_style = 1,
            fill_style = 3004,
            )

DCH300.xsec  = 0.020179   
DCH400.xsec  = 0.0059727  
DCH500.xsec  = 0.0021733  
DCH600.xsec  = 0.00089447 
DCH700.xsec  = 0.00040462 
DCH800.xsec  = 0.00019397 
DCH900.xsec  = 9.8716e-05 
DCH1000.xsec = 5.2052e-05
DCH1100.xsec = 2.8246e-05
DCH1200.xsec = 1.5651e-05
DCH1300.xsec = 8.877e-06 

list_DCH =[globals()[DCH_name%(m)] for m in DCH_masses]

all_DCH = Sample( name =  'all_DCH',
                    tlatex = 'm_{H^{\pm\pm}}=all',
                    line_color = ROOT.kOrange-3,
                    marker_color = ROOT.kOrange-3,
                    fill_color = ROOT.kOrange-3,
                    line_width  = 3,
                    line_style = 1,
                    fill_style = 3004,
                    daughters = list_DCH
                ) 

single_DCH = [DCH500]

#-------------------------------------------------------------------------------
# Collections 
#-------------------------------------------------------------------------------

all_data = data.daughters

all_mc = []
#all_mc += mytestSample.daughters
all_mc += diboson_sherpa.daughters
all_mc += diboson_powheg.daughters

all_mc += Wenu.daughters
all_mc += Wmunu.daughters
all_mc += Wtaunu.daughters

all_mc += WenuPowheg.daughters
all_mc += WmunuPowheg.daughters
all_mc += WtaunuPowheg.daughters

all_mc += Zee.daughters
all_mc += Zmumu.daughters
all_mc += Ztautau.daughters

all_mc += ZeePowheg.daughters
all_mc += ZmumuPowheg.daughters
all_mc += ZtautauPowheg.daughters

#####all_mc += ttX.daughters
#all_mc += singletop.daughters
#####all_mc += ttbar.daughters
#####all_mc += all_DCH.daughters
#####all_mc += single_DCH

## EOF
